"""
Mock MCP client.

Simulates the tools that the real Product MCP Server (Task 4, built by a
teammate) will expose, using the exact same input/output shapes agreed in
the team's MCP contract. Swap this module for a real MCP client once the
teammate's server is ready — `agent.py` should not need to change.

Contract reference (docs/mcp_contract.md — to be written/validated with the
teammate building Task 4):

  list_products(category: str | None) -> {"products": [...]}
  search_products(query: str) -> {"products": [...]}
  get_product_details(product_id: str) -> {...} | {"error": "not_found"}
  check_stock(product_id: str, branch_id: str | None) -> {"stock": [...]}
  list_branch_inventory(branch_id: str) -> {"items": [...]} | {"error": "not_found"}
"""

_FAKE_PRODUCTS = {
    "HB-LAP-1001": {
        "id": "HB-LAP-1001",
        "name": "Laptop Pro 15",
        "description": "15-inch laptop, 16GB RAM, 512GB SSD.",
        "price": 1299.99,
        "category": "electronics",
        "supplier": "TechCorp",
    },
    "HB-KEY-2003": {
        "id": "HB-KEY-2003",
        "name": "Mechanical Keyboard",
        "description": "Backlit mechanical keyboard, blue switches.",
        "price": 89.90,
        "category": "electronics",
        "supplier": "TechCorp",
    },
}

_FAKE_STOCK = {
    "HB-LAP-1001": [
        {"branch_id": "BR-1", "branch_name": "Paris-Nord", "quantity": 12},
        {"branch_id": "BR-2", "branch_name": "Lyon-Centre", "quantity": 0},
    ],
    "HB-KEY-2003": [
        {"branch_id": "BR-1", "branch_name": "Paris-Nord", "quantity": 5},
        {"branch_id": "BR-2", "branch_name": "Lyon-Centre", "quantity": 20},
    ],
}

_FAKE_BRANCH_INVENTORY = {
    "BR-1": [
        {"product_id": "HB-LAP-1001", "quantity": 12},
        {"product_id": "HB-KEY-2003", "quantity": 5},
    ],
    "BR-2": [
        {"product_id": "HB-KEY-2003", "quantity": 20},
    ],
}


def list_products(category: str | None = None) -> dict:
    products = list(_FAKE_PRODUCTS.values())
    if category:
        products = [p for p in products if p["category"] == category]
    return {"products": products}


def search_products(query: str) -> dict:
    query_lower = query.lower()
    products = [
        p for p in _FAKE_PRODUCTS.values() if query_lower in p["name"].lower()
    ]
    return {"products": products}


def get_product_details(product_id: str) -> dict:
    product = _FAKE_PRODUCTS.get(product_id)
    if product is None:
        return {"error": "not_found"}
    return product


def check_stock(product_id: str, branch_id: str | None = None) -> dict:
    stock = _FAKE_STOCK.get(product_id, [])
    if branch_id:
        stock = [s for s in stock if s["branch_id"] == branch_id]
    return {"stock": stock}


def list_branch_inventory(branch_id: str) -> dict:
    items = _FAKE_BRANCH_INVENTORY.get(branch_id)
    if items is None:
        return {"error": "not_found"}
    return {"items": items}
