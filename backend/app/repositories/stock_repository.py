from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Stock


def get_stock(db: Session, branch_id: int, product_id: str) -> Stock | None:
    return db.scalar(select(Stock).where(Stock.branch_id == branch_id, Stock.product_id == product_id))


def list_stocks_by_branch(db: Session, branch_id: int) -> list[Stock]:
    return list(db.scalars(select(Stock).where(Stock.branch_id == branch_id).order_by(Stock.product_id)))


def list_stocks_by_product(db: Session, product_id: str) -> list[Stock]:
    return list(db.scalars(select(Stock).where(Stock.product_id == product_id).order_by(Stock.branch_id)))



def save_stock(db: Session, stock: Stock) -> Stock:
    db.add(stock)
    db.commit()
    db.refresh(stock)
    return stock
