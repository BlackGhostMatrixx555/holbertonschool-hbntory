from fastapi import APIRouter, Depends, Form, Request, responses, status
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from app.database import get_db
from app.models import User, UserRole, Branch
from app.auth import hash_password
from app.dependencies import require_admin

router = APIRouter(tags=["Admin"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/users")
def list_users(request: Request, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    users = db.query(User).filter(User.is_active == True).all()
    branches = db.query(Branch).all()
    return templates.TemplateResponse("admin_dashboard.html", {
        "request": request, 
        "users": users, 
        "branches": branches,
        "current_user": current_user
    })

@router.post("/users/create")
def create_user(
    username: str = Form(...),
    password: str = Form(...),
    branch_id: int = Form(...),
    db: Session = Depends(get_db),
    _: User = Depends(require_admin)
):
    existing = db.query(User).filter(User.username == username).first()
    if existing:
        return responses.RedirectResponse(url="/admin/users?error=Username taken", status_code=status.HTTP_303_SEE_OTHER)

    new_user = User(
        username=username,
        password_hash=hash_password(password),
        role=UserRole.COMMON,
        branch_id=branch_id,
        is_active=True
    )
    db.add(new_user)
    db.commit()
    return responses.RedirectResponse(url="/admin/users", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/users/{user_id}/delete")
def soft_delete_user(user_id: int, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    user = db.query(User).filter(User.id == user_id).first()
    if user and user.role != UserRole.ADMIN:
        user.is_active = False
        db.commit()
    return responses.RedirectResponse(url="/admin/users", status_code=status.HTTP_303_SEE_OTHER)
