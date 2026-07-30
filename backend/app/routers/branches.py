from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, require_admin
from app.models import User
from app.schemas import BranchCreate, BranchResponse, BranchUpdate
from app.services import branch_service

router = APIRouter(prefix="/branches", tags=["branches"])


@router.get("", response_model=list[BranchResponse])
def list_all(_: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return branch_service.get_branches(db)


@router.post("", response_model=BranchResponse, status_code=status.HTTP_201_CREATED)
def create(data: BranchCreate, _: User = Depends(require_admin), db: Session = Depends(get_db)):
    return branch_service.create_branch(db, data)


@router.put("/{branch_id}", response_model=BranchResponse)
def update(branch_id: int, data: BranchUpdate, _: User = Depends(require_admin), db: Session = Depends(get_db)):
    return branch_service.update_branch(db, branch_id, data)
