# HBntory Backend

Backend REST FastAPI pour l’authentification, les utilisateurs, les agences et les stocks.

## Lancement local

```bash
cp .env.example .env
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Documentation : http://localhost:8000/docs

## Comptes de démonstration

- admin / Admin123!
- employee / Employee123!

## Tests

```bash
pytest -q
```

## Routes principales

- POST /auth/login
- GET /auth/me
- GET/POST/PUT/DELETE /users
- GET/POST/PUT /branches
- GET /stocks
- POST /stocks/add
- POST /stocks/remove
- GET /internal/stocks/product/{product_id}
