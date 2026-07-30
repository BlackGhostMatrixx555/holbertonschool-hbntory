from fastapi import APIRouter, Depends, Form, Request, Response, responses, status
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from app.database import get_db
from app.models import User
from app.auth import verify_password, create_access_token

router = APIRouter(tags=["Auth"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
def login(
    response: Response,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username, User.is_active == True).first()
    if not user or not verify_password(password, user.password_hash):
        return responses.RedirectResponse(url="/login?error=Invalid credentials", status_code=status.HTTP_303_SEE_OTHER)

    token = create_access_token({"sub": user.username, "role": user.role.value})
    
    target_url = "/admin/users" if user.role.value == "admin" else "/stock/dashboard"
    res = responses.RedirectResponse(url=target_url, status_code=status.HTTP_303_SEE_OTHER)
    res.set_cookie(key="access_token", value=token, httponly=True)
    return res

@router.get("/logout")
def logout():
    res = responses.RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    res.delete_cookie("access_token")
    return res
