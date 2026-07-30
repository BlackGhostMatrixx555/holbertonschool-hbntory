from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Branch


def get_branch_by_id(db: Session, branch_id: int) -> Branch | None:
    return db.get(Branch, branch_id)


def get_branch_by_name(db: Session, name: str) -> Branch | None:
    return db.scalar(select(Branch).where(Branch.name == name))


def list_branches(db: Session) -> list[Branch]:
    return list(db.scalars(select(Branch).order_by(Branch.name)))


def add_branch(db: Session, branch: Branch) -> Branch:
    db.add(branch)
    db.commit()
    db.refresh(branch)
    return branch


def save_branch(db: Session, branch: Branch) -> Branch:
    db.add(branch)
    db.commit()
    db.refresh(branch)
    return branch
