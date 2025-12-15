#!/usr/bin/env python
"""Test script to verify the MCP server is working correctly."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_server():
    """Test all server functionality."""
    print("Testing Shopping Agent MCP Server\n")

    # Import server functions
    try:
        from src.main import hello, placeholder_tool
        print("[OK] Server modules imported successfully")
    except ImportError as e:
        print(f"[ERROR] Failed to import server: {e}")
        return False

    # Test 1: Hello tool
    print("\nTest 1: Hello tool...")
    result = hello("World")
    if result == "Hello, World!":
        print(f"[OK] hello('World') = '{result}'")
    else:
        print(f"[ERROR] Unexpected result: {result}")
        return False

    # Test 2: Placeholder tool
    print("\nTest 2: Placeholder tool...")
    result = placeholder_tool("test")
    if result.get("status") == "success":
        print(f"[OK] placeholder_tool('test') = {result}")
    else:
        print(f"[ERROR] Unexpected result: {result}")
        return False

    print("\n" + "=" * 50)
    print("[SUCCESS] All tests passed! Server is ready.")

    return True


if __name__ == "__main__":
    success = test_server()
    sys.exit(0 if success else 1)
