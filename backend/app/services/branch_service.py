from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Branch
from app.repositories.branch_repository import add_branch, get_branch_by_id, get_branch_by_name, list_branches, save_branch
from app.schemas import BranchCreate, BranchUpdate


def create_branch(db: Session, data: BranchCreate) -> Branch:
    if get_branch_by_name(db, data.name):
        raise HTTPException(status_code=409, detail="Branch name already exists")
    return add_branch(db, Branch(name=data.name, address=data.address))


def get_branches(db: Session) -> list[Branch]:
    return list_branches(db)


def update_branch(db: Session, branch_id: int, data: BranchUpdate) -> Branch:
    branch = get_branch_by_id(db, branch_id)
    if branch is None:
        raise HTTPException(status_code=404, detail="Branch not found")
    values = data.model_dump(exclude_unset=True)
    if "name" in values and values["name"] != branch.name and get_branch_by_name(db, values["name"]):
        raise HTTPException(status_code=409, detail="Branch name already exists")
    for key, value in values.items():
        setattr(branch, key, value)
    return save_branch(db, branch)
