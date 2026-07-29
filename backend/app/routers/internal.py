from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_internal_api_key
from app.schemas import BranchResponse, StockResponse
from app.services import branch_service, stock_service

router = APIRouter(prefix="/internal", tags=["internal"], dependencies=[Depends(require_internal_api_key)])


@router.get("/branches", response_model=list[BranchResponse])
def list_branches(db: Session = Depends(get_db)):
    return branch_service.get_branches(db)


@router.get("/stocks/product/{product_id}", response_model=list[StockResponse])
def product_availability(product_id: str, db: Session = Depends(get_db)):
    return stock_service.get_product_availability(db, product_id)


@router.get("/stocks/branch/{branch_id}", response_model=list[StockResponse])
def branch_stocks(branch_id: int, db: Session = Depends(get_db)):
    return stock_service.get_branch_stocks(db, branch_id)

