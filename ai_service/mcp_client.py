"""
Real data client for the AI service.

This keeps the same function contract as mcp_client_mock.py, but reads from
the HBntory backend internal API and the product API used by the MCP server.
"""

import os
from typing import Any

import httpx


PRODUCT_API_URL = os.getenv("PRODUCT_API_URL", "http://localhost:8001")
BACKEND_INTERNAL_URL = os.getenv("BACKEND_INTERNAL_URL", "http://localhost:8000/internal")
INTERNAL_API_KEY = os.getenv("INTERNAL_API_KEY", "change-internal-key")


def _headers() -> dict[str, str]:
    return {"X-Internal-API-Key": INTERNAL_API_KEY}


def list_products(category: str | None = None) -> dict[str, Any]:
    try:
        with httpx.Client(timeout=5.0) as client:
            response = client.get(f"{PRODUCT_API_URL.rstrip('/')}/products")
            response.raise_for_status()
            products = response.json()
    except Exception as exc:
        return {"products": [], "error": str(exc)}

    if category:
        products = [
            product
            for product in products
            if str(product.get("category", "")).lower() == category.lower()
        ]
    return {"products": products}


def search_products(query: str) -> dict[str, Any]:
    products = list_products().get("products", [])
    query_lower = query.lower()
    return {
        "products": [
            product
            for product in products
            if query_lower in str(product.get("name", "")).lower()
            or query_lower in str(product.get("description", "")).lower()
            or query_lower in str(product.get("id", "")).lower()
        ]
    }


def get_product_details(product_id: str) -> dict[str, Any]:
    try:
        with httpx.Client(timeout=5.0) as client:
            response = client.get(f"{PRODUCT_API_URL.rstrip('/')}/products/{product_id}")
            response.raise_for_status()
            data = response.json()
    except Exception as exc:
        return {"error": str(exc)}

    if data.get("error") == "not_found":
        return {"error": "not_found"}
    return data


def check_stock(product_id: str, branch_id: str | None = None) -> dict[str, Any]:
    try:
        with httpx.Client(timeout=5.0) as client:
            response = client.get(
                f"{BACKEND_INTERNAL_URL.rstrip('/')}/stocks/product/{product_id}",
                headers=_headers(),
            )
            response.raise_for_status()
            stock = response.json()
    except Exception as exc:
        return {"stock": [], "error": str(exc)}

    formatted = [
        {
            "branch_id": str(item["branch_id"]),
            "branch_name": item.get("branch_name") or f"Branch {item['branch_id']}",
            "quantity": item["quantity"],
        }
        for item in stock
    ]
    if branch_id:
        resolved_branch_id = _resolve_branch_id(branch_id)
        formatted = [
            item
            for item in formatted
            if item["branch_id"] == str(resolved_branch_id or branch_id)
        ]
    return {"stock": formatted}


def list_branch_inventory(branch_id: str) -> dict[str, Any]:
    resolved_branch_id = _resolve_branch_id(branch_id)
    if resolved_branch_id is None:
        return {"error": "not_found"}

    try:
        with httpx.Client(timeout=5.0) as client:
            response = client.get(
                f"{BACKEND_INTERNAL_URL.rstrip('/')}/stocks/branch/{resolved_branch_id}",
                headers=_headers(),
            )
            response.raise_for_status()
            items = response.json()
    except Exception as exc:
        return {"items": [], "error": str(exc)}

    return {
        "items": [
            {"product_id": item["product_id"], "quantity": item["quantity"]}
            for item in items
        ]
    }


def _resolve_branch_id(branch_identifier: str | int) -> int | None:
    if isinstance(branch_identifier, int):
        return branch_identifier

    clean = str(branch_identifier).strip()
    if clean.isdigit():
        return int(clean)
    if clean.upper().startswith("BR-"):
        code = clean[3:].lstrip("0")
        if code.isdigit():
            return int(code)

    try:
        with httpx.Client(timeout=5.0) as client:
            response = client.get(
                f"{BACKEND_INTERNAL_URL.rstrip('/')}/branches",
                headers=_headers(),
            )
            response.raise_for_status()
            branches = response.json()
    except Exception:
        return None

    for branch in branches:
        if str(branch["id"]) == clean or branch["name"].lower() == clean.lower():
            return branch["id"]
    return None
