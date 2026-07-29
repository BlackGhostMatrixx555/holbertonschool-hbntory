from sqlalchemy.orm import Session

from app.models import Branch, Stock, User, UserRole
from app.repositories.branch_repository import get_branch_by_name
from app.repositories.stock_repository import get_stock
from app.repositories.user_repository import get_user_by_username
from app.security import hash_password


def seed_database(db: Session) -> None:
    paris = get_branch_by_name(db, "Paris")
    if paris is None:
        paris = Branch(name="Paris", address="Paris, France")
        db.add(paris)
    lyon = get_branch_by_name(db, "Lyon")
    if lyon is None:
        lyon = Branch(name="Lyon", address="Lyon, France")
        db.add(lyon)
    db.commit()
    db.refresh(paris)
    db.refresh(lyon)

    if get_user_by_username(db, "admin") is None:
        db.add(User(username="admin", password_hash=hash_password("Admin123!"), role=UserRole.ADMIN))
    if get_user_by_username(db, "employee") is None:
        db.add(User(username="employee", password_hash=hash_password("Employee123!"), role=UserRole.COMMON, branch_id=paris.id))

    sample_stocks = [
        (paris.id, "HB-LAP-1001", 10),
        (paris.id, "HB-KEY-2003", 25),
        (lyon.id, "HB-LAP-1001", 5),
        (lyon.id, "HB-MON-3005", 12),
    ]
    for branch_id, product_id, qty in sample_stocks:
        if get_stock(db, branch_id, product_id) is None:
            db.add(Stock(branch_id=branch_id, product_id=product_id, quantity=qty))

    db.commit()

