from fastapi import APIRouter, Depends, Form, Request, responses, status
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from app.database import get_db
from app.models import User, Stock
from app.dependencies import require_common

router = APIRouter(tags=["Stock"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/dashboard")
def stock_dashboard(request: Request, db: Session = Depends(get_db), current_user: User = Depends(require_common)):
    stocks = db.query(Stock).filter(Stock.branch_id == current_user.branch_id).all()
    return templates.TemplateResponse("staff_dashboard.html", {
        "request": request,
        "stocks": stocks,
        "branch": current_user.branch,
        "current_user": current_user
    })

@router.post("/update")
def update_stock(
    product_id: str = Form(...),
    delta: int = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_common)
):
    stock = db.query(Stock).filter(
        Stock.branch_id == current_user.branch_id,
        Stock.product_id == product_id
    ).first()

    if not stock:
        if delta < 0:
            return responses.RedirectResponse(url="/stock/dashboard?error=Cannot remove nonexistent stock", status_code=status.HTTP_303_SEE_OTHER)
        stock = Stock(branch_id=current_user.branch_id, product_id=product_id, quantity=delta)
        db.add(stock)
    else:
        new_quantity = stock.quantity + delta
        if new_quantity < 0:
            return responses.RedirectResponse(url="/stock/dashboard?error=Stock cannot be negative", status_code=status.HTTP_303_SEE_OTHER)
        stock.quantity = new_quantity

    db.commit()
    return responses.RedirectResponse(url="/stock/dashboard", status_code=status.HTTP_303_SEE_OTHER)
