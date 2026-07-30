import sys
from mcp.server.fastmcp import FastMCP
import client

mcp = FastMCP("HBntory Product & Stock MCP Server")


@mcp.tool()
def get_product_details(product_id: str) -> dict:
    """Get detailed information about a product by its ID (e.g., 'HB-LAP-1001').

    Args:
        product_id: Unique product identifier string.
    """
    return client.get_product_details(product_id)


@mcp.tool()
def list_products() -> list | dict:
    """List all products available in the external catalog."""
    return client.list_products()


@mcp.tool()
def check_stock(product_id: str) -> dict:
    """Check availability and quantities for a product across all store branches.

    Args:
        product_id: Unique product identifier string.
    """
    return client.check_stock(product_id)


@mcp.tool()
def list_branch_inventory(branch_identifier: str) -> dict:
    """List all products currently in stock for a specific branch.

    Args:
        branch_identifier: Branch name (e.g., 'Paris', 'Lyon') or branch ID (e.g., 'BR-01', '1').
    """
    return client.list_branch_inventory(branch_identifier)


@mcp.tool()
def list_branches() -> list:
    """List all physical store branches."""
    return client.list_branches()


if __name__ == "__main__":
    mcp.run()
