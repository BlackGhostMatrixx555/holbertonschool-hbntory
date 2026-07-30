import httpx
from typing import Any
from config import settings


def _get_headers() -> dict[str, str]:
    return {"X-Internal-API-Key": settings.internal_api_key}


def get_product_details(product_id: str) -> dict[str, Any]:
    """Fetch product details from the external Product API."""
    url = f"{settings.product_api_url.rstrip('/')}/products/{product_id}"
    try:
        with httpx.Client(timeout=5.0) as client:
            res = client.get(url)
            if res.status_code == 404:
                return {"error": "not_found"}
            res.raise_for_status()
            return res.json()
    except Exception as e:
        return {"error": f"Failed to fetch product details: {str(e)}"}


def list_products() -> list[dict[str, Any]] | dict[str, Any]:
    """Fetch the product list from the external Product API."""
    url = f"{settings.product_api_url.rstrip('/')}/products"
    try:
        with httpx.Client(timeout=5.0) as client:
            res = client.get(url)
            res.raise_for_status()
            return res.json()
    except Exception as e:
        return {"error": f"Failed to list products: {str(e)}"}


def list_branches() -> list[dict[str, Any]]:
    """Fetch all active branches from the backend internal API."""
    url = f"{settings.backend_internal_url.rstrip('/')}/branches"
    try:
        with httpx.Client(timeout=5.0) as client:
            res = client.get(url, headers=_get_headers())
            res.raise_for_status()
            return res.json()
    except Exception:
        return []


def resolve_branch_id(branch_identifier: str | int) -> int | None:
    """Resolve a branch name (e.g., 'Paris', 'BR-01', '1') to an integer branch_id."""
    if isinstance(branch_identifier, int):
        return branch_identifier
    if str(branch_identifier).isdigit():
        return int(branch_identifier)
    
    # Clean identifier e.g., "BR-01" -> "1" or "Paris" -> matching name
    clean = str(branch_identifier).strip()
    if clean.upper().startswith("BR-"):
        code = clean[3:].lstrip("0")
        if code.isdigit():
            return int(code)

    branches = list_branches()
    for b in branches:
        if b["name"].lower() == clean.lower() or str(b["id"]) == clean:
            return b["id"]
    return None


def check_stock(product_id: str) -> dict[str, Any]:
    """Fetch availability for a product across all branches from the backend internal API."""
    url = f"{settings.backend_internal_url.rstrip('/')}/stocks/product/{product_id}"
    try:
        with httpx.Client(timeout=5.0) as client:
            res = client.get(url, headers=_get_headers())
            res.raise_for_status()
            stocks = res.json()
            # Standardize output for the AI agent
            formatted_stock = [
                {
                    "branch_id": str(item["branch_id"]),
                    "branch_name": item.get("branch_name") or f"Branch {item['branch_id']}",
                    "quantity": item["quantity"],
                }
                for item in stocks
            ]
            return {"stock": formatted_stock}
    except Exception as e:
        return {"stock": [], "error": f"Failed to fetch stock: {str(e)}"}


def list_branch_inventory(branch_identifier: str | int) -> dict[str, Any]:
    """Fetch all stock entries for a specific branch from the backend internal API."""
    bid = resolve_branch_id(branch_identifier)
    if bid is None:
        return {"error": "not_found"}

    url = f"{settings.backend_internal_url.rstrip('/')}/stocks/branch/{bid}"
    try:
        with httpx.Client(timeout=5.0) as client:
            res = client.get(url, headers=_get_headers())
            if res.status_code == 404:
                return {"error": "not_found"}
            res.raise_for_status()
            items = res.json()
            return {"items": [{"product_id": item["product_id"], "quantity": item["quantity"]} for item in items]}
    except Exception as e:
        return {"items": [], "error": str(e)}
