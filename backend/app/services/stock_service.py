from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Stock
from app.repositories.stock_repository import get_stock, list_stocks_by_branch, list_stocks_by_product, save_stock


def get_branch_stocks(db: Session, branch_id: int) -> list[Stock]:
    return list_stocks_by_branch(db, branch_id)


def add_stock(db: Session, branch_id: int, product_id: str, quantity: int) -> Stock:
    stock = get_stock(db, branch_id, product_id)
    if stock is None:
        stock = Stock(branch_id=branch_id, product_id=product_id, quantity=0)
    stock.quantity += quantity
    return save_stock(db, stock)


def remove_stock(db: Session, branch_id: int, product_id: str, quantity: int) -> Stock:
    stock = get_stock(db, branch_id, product_id)
    if stock is None:
        raise HTTPException(status_code=404, detail="Stock entry not found")
    if stock.quantity < quantity:
        raise HTTPException(status_code=409, detail="Insufficient stock")
    stock.quantity -= quantity
    return save_stock(db, stock)


def get_product_availability(db: Session, product_id: str) -> list[Stock]:
    return list_stocks_by_product(db, product_id)

