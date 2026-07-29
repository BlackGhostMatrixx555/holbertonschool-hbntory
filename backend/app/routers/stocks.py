from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_common
from app.models import User
from app.schemas import StockChange, StockResponse
from app.services import stock_service

router = APIRouter(prefix="/stocks", tags=["stocks"])


@router.get("", response_model=list[StockResponse])
def my_stocks(user: User = Depends(require_common), db: Session = Depends(get_db)):
    return stock_service.get_branch_stocks(db, user.branch_id)


@router.post("/add", response_model=StockResponse)
def add(data: StockChange, user: User = Depends(require_common), db: Session = Depends(get_db)):
    return stock_service.add_stock(db, user.branch_id, data.product_id, data.quantity)


@router.post("/remove", response_model=StockResponse)
def remove(data: StockChange, user: User = Depends(require_common), db: Session = Depends(get_db)):
    return stock_service.remove_stock(db, user.branch_id, data.product_id, data.quantity)
