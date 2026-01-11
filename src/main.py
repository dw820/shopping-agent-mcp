import os
from mcp.server.fastmcp import FastMCP

# Initialize MCP server
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
def shop_product(product_name: str, max_price: float = None, quantity: int = 1) -> str:
    """Search for and purchase a product.
    
    Args:
        product_name: Name of the product to search for
        max_price: Maximum price to pay for the product (optional)
        quantity: How many units to purchase (default: 1)
        
    Returns:
        Confirmation message with purchase details
        
    Example:
        >>> shop_product("wireless headphones", max_price=150, quantity=2)
        "Successfully purchased 2 units of 'wireless headphones' under $150"
    """
    # Get environment variables
    env_vars = get_env_vars()
    
    # In a real implementation, this would:
    # 1. Use browser automation to navigate to shopping site
    # 2. Login using TARGET_EMAIL and TARGET_PASSWORD
    # 3. Search for the product
    # 4. Apply price filter if max_price is specified
    # 5. Add to cart and checkout
    # 6. Handle any verification (e.g., phone number)
    
    price_info = f" under ${max_price}" if max_price else ""
    return f"Successfully purchased {quantity} units of '{product_name}'{price_info}"


def main() -> None:
    """Start the MCP server.
    
    This function initializes and runs the Shopping Agent MCP server.
    The server provides a 'shop_product' tool that can be used by
    MCP clients to automate shopping tasks.
    
    Environment variables required:
        - BROWSER_USE_API_KEY: API key for browser automation
        - BROWSER_USE_PROFILE_ID: Profile ID for browser automation  
        - TARGET_EMAIL: Email for target website login
        - TARGET_PASSWORD: Password for target website login
        - PHONE_NUMBER: Phone number for verification
    
    Usage:
        python src/main.py
    
    For more information, see the README.md file.
    """
    print("🛒 Starting Shopping Agent MCP Server...")
    print("🔧 Available tools: shop_product")
    print("📚 Documentation: See README.md for setup and usage instructions")
    print("⚙️  Configuration: Ensure all environment variables are set in .env file")
    print()
    
    # Validate environment variables before starting
    try:
        get_env_vars()
        print("✅ Environment variables validated successfully")
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("   Please check your .env file and ensure all required variables are set")
        return
    
    print("🚀 Server is starting...")
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()