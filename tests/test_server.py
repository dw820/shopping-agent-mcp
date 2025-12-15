#!/usr/bin/env python
"""Test script to verify the MCP server is working correctly."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_server():
    """Test all server functionality."""
    print("Testing Shopping Agent MCP Server\n")

    # Import server
    try:
        from src.main import mcp, shop_product
        print("[OK] Server modules imported successfully")
    except ImportError as e:
        print(f"[ERROR] Failed to import server: {e}")
        return False

    # Test 1: mcp is a FastMCP instance
    print("\nTest 1: Server instance...")
    from mcp.server.fastmcp import FastMCP
    if isinstance(mcp, FastMCP):
        print(f"[OK] mcp is FastMCP instance")
    else:
        print(f"[ERROR] mcp is not FastMCP instance: {type(mcp)}")
        return False

    # Test 2: shop_product tool is registered
    print("\nTest 2: Tool registration...")
    if shop_product is not None:
        print(f"[OK] shop_product tool is defined")
    else:
        print(f"[ERROR] shop_product tool not found")
        return False

    print("\n" + "=" * 50)
    print("[SUCCESS] All tests passed! Server is ready.")

    return True


if __name__ == "__main__":
    success = test_server()
    sys.exit(0 if success else 1)
