from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_admin
from app.models import User
from app.schemas import UserCreate, UserResponse, UserUpdate
from app.services import user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserResponse])
def list_all_users(_: User = Depends(require_admin), db: Session = Depends(get_db)):
    return user_service.get_users(db)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create(data: UserCreate, _: User = Depends(require_admin), db: Session = Depends(get_db)):
    return user_service.create_user(db, data)


@router.get("/{user_id}", response_model=UserResponse)
def get_one(user_id: int, _: User = Depends(require_admin), db: Session = Depends(get_db)):
    return user_service.get_user_or_404(db, user_id)


@router.put("/{user_id}", response_model=UserResponse)
def update(user_id: int, data: UserUpdate, _: User = Depends(require_admin), db: Session = Depends(get_db)):
    return user_service.update_user(db, user_id, data)


@router.delete("/{user_id}", response_model=UserResponse)
def deactivate(user_id: int, admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    return user_service.deactivate_user(db, user_id, admin.id)
