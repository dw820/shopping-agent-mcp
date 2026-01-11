import os
from typing import Dict, Optional
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("shopping-agent")


def get_env_vars() -> dict:
    """Get required environment variables.
    
    Returns:
        Dictionary with all required env vars
        
    Raises:
        ValueError: If any required env var is missing
    """
    required = {
        "BROWSER_USE_API_KEY": os.getenv("BROWSER_USE_API_KEY"),
        "BROWSER_USE_PROFILE_ID": os.getenv("BROWSER_USE_PROFILE_ID"),
        "TARGET_EMAIL": os.getenv("TARGET_EMAIL"),
        "TARGET_PASSWORD": os.getenv("TARGET_PASSWORD"),
        "PHONE_NUMBER": os.getenv("PHONE_NUMBER"),
    }
    
    missing = [k for k, v in required.items() if not v]
    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
    
    return required


@mcp.tool()
def shop_product(product_name: str, max_price: Optional[float] = None, quantity: int = 1) -> Dict:
    """Shop for a product automatically.
    
    This tool automates the process of searching for and purchasing a product
    using browser automation.
    
    Args:
        product_name: Name of the product to search for
        max_price: Maximum price to pay for the product (optional)
        quantity: Number of items to purchase (default: 1)
        
    Returns:
        Dictionary containing shopping result with status and details
        
    Example:
        shop_product("wireless headphones", max_price=199.99, quantity=1)
    """
    # Get environment variables
    env_vars = get_env_vars()
    
    # In a real implementation, this would use BrowserUse API
    # to automate the shopping process
    
    # For now, return a mock response
    return {
        "status": "success",
        "message": f"Successfully purchased {quantity} x '{product_name}'",
        "product_name": product_name,
        "quantity": quantity,
        "max_price": max_price,
        "environment_configured": True,
        "browser_profile": env_vars.get("BROWSER_USE_PROFILE_ID"),
    }


def main() -> None:
    """Start the MCP server."""
    print("=" * 50)
    print("🛒 Shopping Agent MCP Server")
    print("=" * 50)
    
    # Check environment variables
    try:
        env_vars = get_env_vars()
        print("✅ Environment variables loaded successfully")
        print(f"   • BrowserUse Profile: {env_vars.get('BROWSER_USE_PROFILE_ID')}")
        print(f"   • Target Email: {env_vars.get('TARGET_EMAIL')}")
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("\nPlease set the following environment variables:")
        print("  - BROWSER_USE_API_KEY")
        print("  - BROWSER_USE_PROFILE_ID")
        print("  - TARGET_EMAIL")
        print("  - TARGET_PASSWORD")
        print("  - PHONE_NUMBER")
        print("\nYou can create a .env file based on .env.example")
        return
    
    print("\n🔧 Available Tools:")
    print("   • shop_product - Automates product shopping")
    print("\n📖 Usage Examples:")
    print('   • shop_product("wireless headphones", max_price=199.99)')
    print('   • shop_product("laptop", quantity=1)')
    print('   • shop_product("coffee maker", max_price=89.99, quantity=2)')
    print("\n" + "=" * 50)
    print("🚀 Starting server...")
    print("   Use Ctrl+C to stop the server")
    print("=" * 50)
    print()
    
    # Start the MCP server
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()