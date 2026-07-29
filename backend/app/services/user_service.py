from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import User, UserRole
from app.repositories.branch_repository import get_branch_by_id
from app.repositories.user_repository import add_user, get_user_by_id, get_user_by_username, list_users, save_user
from app.schemas import UserCreate, UserUpdate
from app.security import hash_password


def _validate_branch(db: Session, role: UserRole, branch_id: int | None) -> None:
    if role == UserRole.COMMON:
        if branch_id is None:
            raise HTTPException(status_code=422, detail="A common user must have a branch")
        branch = get_branch_by_id(db, branch_id)
        if branch is None or not branch.is_active:
            raise HTTPException(status_code=404, detail="Branch not found or inactive")


def create_user(db: Session, data: UserCreate) -> User:
    if get_user_by_username(db, data.username):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
    _validate_branch(db, data.role, data.branch_id)
    user = User(
        username=data.username,
        password_hash=hash_password(data.password),
        role=data.role,
        branch_id=data.branch_id if data.role == UserRole.COMMON else None,
    )
    return add_user(db, user)


def get_users(db: Session) -> list[User]:
    return list_users(db)


def get_user_or_404(db: Session, user_id: int) -> User:
    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def update_user(db: Session, user_id: int, data: UserUpdate) -> User:
    user = get_user_or_404(db, user_id)
    values = data.model_dump(exclude_unset=True)
    if "username" in values and values["username"] != user.username:
        if get_user_by_username(db, values["username"]):
            raise HTTPException(status_code=409, detail="Username already exists")
        user.username = values["username"]
    if "password" in values:
        user.password_hash = hash_password(values.pop("password"))
    role = values.get("role", user.role)
    branch_id = values.get("branch_id", user.branch_id)
    _validate_branch(db, role, branch_id)
    for key, value in values.items():
        setattr(user, key, value)
    if user.role == UserRole.ADMIN:
        user.branch_id = None
    return save_user(db, user)


def deactivate_user(db: Session, user_id: int, current_admin_id: int) -> User:
    if user_id == current_admin_id:
        raise HTTPException(status_code=400, detail="You cannot deactivate your own account")
    user = get_user_or_404(db, user_id)
    user.is_active = False
    return save_user(db, user)
