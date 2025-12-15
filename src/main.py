#!/usr/bin/env python3
"""Shopping Agent - Target.com Browser Automation.

This script uses browser-use-sdk to:
1. Login to Target.com with credentials from environment
2. Skip any popups/prompts after login
3. Add a random item to the shopping cart (without checkout)
"""

import asyncio
import os
from dotenv import load_dotenv
from browser_use_sdk import BrowserUse

# Load environment variables
load_dotenv()


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
    }
    
    missing = [k for k, v in required.items() if not v]
    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
    
    return required


async def run_target_shopping_task():
    """Run the Target.com shopping automation task."""
    
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

3. ADD RANDOM ITEM TO CART:
   - Once on the homepage, browse or search for any product (e.g., "snacks", "toys", "electronics")
   - Click on any product to view its details
   - Add the item to your cart
   
4. VERIFY:
   - Confirm the item was added to cart (you should see cart count increase)
   - DO NOT proceed to checkout
   - Report what item you added to the cart

IMPORTANT: 
- Skip all promotional popups, newsletter signups, and notification requests
- Do not checkout or enter any payment information
- Just add ONE item to the cart and stop
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
        
        print(f"\n✅ Task completed!")
        print(f"   Output: {result.output if hasattr(result, 'output') else result}")
        
    except Exception as e:
        print(f"\n❌ Task failed: {e}")
        raise
    finally:
        print(f"\n🛑 Session complete (profile state preserved)")


async def main():
    """Main entry point."""
    try:
        await run_target_shopping_task()
    except ValueError as e:
        print(f"\n⚠️ Configuration error: {e}")
        print("   Please check your .env file has all required variables.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
