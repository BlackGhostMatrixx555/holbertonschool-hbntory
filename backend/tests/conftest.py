import os
os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"
os.environ["JWT_SECRET_KEY"] = "test-secret"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.models import Branch, User, UserRole
from app.security import hash_password

engine = create_engine("sqlite+pysqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


def override_get_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with TestingSession() as db:
        branch = Branch(name="Paris", address="Paris")
        db.add(branch)
        db.commit(); db.refresh(branch)
        db.add_all([
            User(username="admin", password_hash=hash_password("Admin123!"), role=UserRole.ADMIN),
            User(username="employee", password_hash=hash_password("Employee123!"), role=UserRole.COMMON, branch_id=branch.id),
        ])
        db.commit()
    yield


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


def login(client, username, password):
    response = client.post("/auth/login", json={"username": username, "password": password})
    return response.json()["access_token"]


@pytest.fixture
def admin_headers(client):
    return {"Authorization": f"Bearer {login(client, 'admin', 'Admin123!')}"}


@pytest.fixture
def employee_headers(client):
    return {"Authorization": f"Bearer {login(client, 'employee', 'Employee123!')}"}
