import os
from fastapi import FastAPI, responses, status
from fastapi.staticfiles import StaticFiles
from app.database import engine, Base, SessionLocal
from app.models import User, UserRole, Branch
from app.auth import hash_password
from app.routers import auth, admin, stock

Base.metadata.create_all(bind=engine)

app = FastAPI(title="HBntory Backoffice")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(auth.router)
app.include_router(admin.router, prefix="/admin")
app.include_router(stock.router, prefix="/stock")

@app.get("/")
def root():
    return responses.RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

@app.on_event("startup")
def seed_data():
    db = SessionLocal()
    try:
        if not db.query(Branch).first():
            b1 = Branch(name="Downtown Branch")
            b2 = Branch(name="Uptown Branch")
            db.add_all([b1, b2])
            db.commit()

        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            admin_user = User(
                username="admin",
                password_hash=hash_password("admin123"),
                role=UserRole.ADMIN,
                is_active=True
            )
            db.add(admin_user)
            db.commit()
    finally:
        db.close()
