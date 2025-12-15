#!/usr/bin/env python3
"""Shopping Agent MCP Server - Target.com Browser Automation.

This MCP server exposes a tool that uses browser-use-sdk to:
1. Login to Target.com with credentials from environment
2. Skip any popups/prompts after login
3. Search for a product, add to cart, and proceed to checkout
"""

import asyncio
import logging
import os
from dotenv import load_dotenv
from browser_use_sdk import BrowserUse
from mcp.server.fastmcp import FastMCP

# Load environment variables
load_dotenv()

# Suppress logs for clean output
for logger_name in ("mcp", "httpx", "uvicorn", "uvicorn.access", "uvicorn.error"):
    logging.getLogger(logger_name).setLevel(logging.CRITICAL)

# Create the MCP server
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


async def run_target_shopping_task(
    product_name: str,
    first_name: str,
    last_name: str,
    address: str,
    unit: str,
    city: str,
    state: str,
    zip_code: str,
) -> str:
    """Run the Target.com shopping automation task.
    
    Args:
        product_name: Product to search for
        first_name: Shipping first name
        last_name: Shipping last name
        address: Street address
        unit: Apartment/unit number
        city: City name
        state: State abbreviation (e.g., CA)
        zip_code: ZIP code
        
    Returns:
        Result message describing what was accomplished
    """
    
    # Get environment variables
    env = get_env_vars()
    
    # Initialize the client
    client = BrowserUse(api_key=env["BROWSER_USE_API_KEY"])
    profile_id = env["BROWSER_USE_PROFILE_ID"]
    
    print("🎯 Target.com Shopping Agent")
    print("=" * 50)
    print(f"♻️ Using profile: {profile_id}")
    
    # Create a session with the profile
    print(f"\n📍 Creating session...")
    session = client.sessions.create_session(profile_id=profile_id)
    print(f"   Session ID: {session.id}")
    
    # Build the task prompt with login credentials
    task_prompt = f"""
Go to Target.com (https://www.target.com) and complete the following steps:

1. LOGIN:
   - Click on the account/sign-in button
   - Enter email: {env["TARGET_EMAIL"]}
   - Enter password: {env["TARGET_PASSWORD"]}
   - Submit the login form
   
2. SKIP ALL POPUPS:
   - After login, you may see various popups, modals, or prompts
   - Skip ALL of them by clicking "Maybe Later", "No Thanks", "Skip", "X", or any dismiss button
   - Do NOT sign up for anything extra, do NOT enable notifications
   - Your goal is to get to the main Target homepage as quickly as possible

3. SEARCH AND FIND PRODUCT:
   - Use the search bar to search for: "{product_name}"
   - Look through the search results
   - Find the product that is:
     a) Most relevant/similar to "{product_name}"
     b) Has the LOWEST price among the relevant options
   - If there are multiple similar products, prioritize the cheapest one
   - Click on that product to view its details

4. ADD TO CART:
   - Add the selected item to your cart
   - Confirm the item was added to cart (you should see cart count increase)

5. PROCEED TO CHECKOUT:
   - Click on the cart icon to view your cart
   - Click "Checkout" or "I'm ready to check out" button
   - If asked to select a shipping method, choose "Shipping" (not pickup)

6. FILL SHIPPING ADDRESS:
   - Fill in the shipping address form with the following information:
     - First Name: {first_name}
     - Last Name: {last_name}
     - Address: {address}
     - Apartment/Unit: {unit}
     - City: {city}
     - State: {state}
     - ZIP Code: {zip_code}
     - Phone Number: {env["PHONE_NUMBER"]}
   - Save or continue to the next step after filling the address

7. STOP AND SCREENSHOT:
   - Once you reach the final order review page (where you can see "Place your order" button)
   - Take a screenshot of the page
   - DO NOT click "Place your order" - stop here
   - Report what item is in the cart and the total amount

IMPORTANT: 
- Skip all promotional popups, newsletter signups, and notification requests
- If you see ANY feedback popup like "Got a minute?" or survey requests, immediately click "No Thanks", "X", or any close/dismiss button - do NOT engage with them
- DO NOT click "Place your order" - only go up to the final review page
- If asked for payment info, you can skip or use any saved payment method, but DO NOT complete the purchase
"""

    try:
        # Create and run the task
        print(f"\n🛒 Starting shopping task...")
        task = client.tasks.create_task(
            session_id=session.id,
            llm="browser-use-llm",
            task=task_prompt
        )
        
        print(f"   Task ID: {task.id}")
        print(f"   Status: Running... (this may take a few minutes)")
        
        # Wait for the task to complete
        result = task.complete()
        
        output = result.output if hasattr(result, 'output') else str(result)
        print(f"\n✅ Task completed!")
        print(f"   Output: {output}")
        
        return f"Shopping task completed successfully. {output}"
        
    except Exception as e:
        error_msg = f"Task failed: {e}"
        print(f"\n❌ {error_msg}")
        return error_msg
    finally:
        print(f"\n🛑 Session complete (profile state preserved)")



@mcp.tool()
async def shop_product(
    product_name: str,
    first_name: str,
    last_name: str,
    address: str,
    unit: str,
    city: str,
    state: str,
    zip_code: str,
) -> str:
    """Shop for a product on Target.com and proceed to checkout.
    
    This tool will:
    1. Login to Target.com
    2. Search for the specified product
    3. Find the cheapest relevant option
    4. Add it to cart
    5. Proceed to checkout with the provided shipping address
    6. Stop at the final review page (does NOT complete the purchase)
    
    Args:
        product_name: The product to search for (e.g., "protein bars")
        first_name: Shipping first name
        last_name: Shipping last name
        address: Street address (e.g., "101 Polk St")
        unit: Apartment/unit number (e.g., "Unit 1113")
        city: City name (e.g., "San Francisco")
        state: State abbreviation (e.g., "CA")
        zip_code: ZIP code (e.g., "94102")
        
    Returns:
        A message describing what was accomplished and the order total
    """
    return await run_target_shopping_task(
        product_name=product_name,
        first_name=first_name,
        last_name=last_name,
        address=address,
        unit=unit,
        city=city,
        state=state,
        zip_code=zip_code,
    )


def main() -> None:
    """Start the MCP server."""
    print("🛒 Starting Shopping Agent MCP Server...")
    print("🔧 Available tools: shop_product")
    print()
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()

