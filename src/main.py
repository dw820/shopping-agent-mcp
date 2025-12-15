#!/usr/bin/env python3
"""Shopping Agent MCP Server.

This server provides tools for:
- TODO: Add your tool descriptions here
"""

from __future__ import annotations

import asyncio
import logging

from mcp.server.fastmcp import FastMCP

# Suppress logs for clean output
for logger_name in ("mcp", "httpx", "uvicorn", "uvicorn.access", "uvicorn.error"):
    logging.getLogger(logger_name).setLevel(logging.CRITICAL)

server = FastMCP("shopping-agent")


# =============================================================================
# TOOLS - Add your MCP tools here
# =============================================================================

@server.tool()
def hello(name: str) -> str:
    """Greet someone - placeholder tool.
    
    Args:
        name: The name to greet
        
    Returns:
        A greeting message
    """
    return f"Hello, {name}!"


@server.tool()
def placeholder_tool(param: str) -> dict:
    """Placeholder tool - replace with your implementation.
    
    Args:
        param: A parameter for the tool
        
    Returns:
        A dictionary with the result
    """
    # TODO: Implement your tool logic here
    return {"status": "success", "param": param}


# =============================================================================
# RESOURCES - Add your MCP resources here (optional)
# =============================================================================

# @server.resource("data://{path}")
# def get_data(path: str) -> str:
#     """Serve data files."""
#     # TODO: Implement resource serving
#     pass


# =============================================================================
# MAIN
# =============================================================================

async def main() -> None:
    """Start the MCP server."""
    print("🚀 Starting Shopping Agent MCP Server...")
    print("📡 Transport: streamable-http")
    print("🔧 Available tools: hello, placeholder_tool")
    print()
    await server.serve(transport="streamable-http", verbose=False, log_level="critical")


if __name__ == "__main__":
    asyncio.run(main())
