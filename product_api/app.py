"""
Placeholder Product API — for local development only.

This is a stand-in for the real hbtn-edu/hbntory-products-api Docker image.
Swap this whole service for the real one before final submission — see
docs/COMPATIBILITY_REPORT.md.
"""

from fastapi import FastAPI

app = FastAPI(title="HBntory Product API (placeholder)")

PRODUCTS = {
    "HB-LAP-1001": {
        "id": "HB-LAP-1001",
        "name": "Laptop Pro 15",
        "description": "High performance laptop, 16GB RAM",
        "price": 1200.0,
        "category": "Computers",
    },
    "HB-KEY-2003": {
        "id": "HB-KEY-2003",
        "name": "Mechanical Keyboard",
        "description": "RGB Mechanical Keyboard",
        "price": 85.0,
        "category": "Accessories",
    },
    "HB-MON-3005": {
        "id": "HB-MON-3005",
        "name": "4K Monitor 27 inch",
        "description": "UHD IPS Display",
        "price": 350.0,
        "category": "Displays",
    },
}


@app.get("/products")
def list_products():
    return list(PRODUCTS.values())


@app.get("/products/{product_id}")
def get_product(product_id: str):
    return PRODUCTS.get(product_id, {"error": "not_found"})
