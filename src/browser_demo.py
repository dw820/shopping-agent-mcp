#!/usr/bin/env python3
"""Browser Use Demo with Profile Support.

This script demonstrates using browser-use-sdk with profiles to:
1. Use a persistent profile for login state
2. Open Google Maps
3. Search for "101 Polk St"
"""

import asyncio
import os
from dotenv import load_dotenv
from browser_use_sdk import BrowserUse

# Load environment variables
load_dotenv()


async def search_google_maps(address: str = "101 Polk St"):
    """Open Google Maps and search for an address.
    
    Args:
        address: The address to search for
    """
    # Get API key and profile ID from environment
    api_key = os.getenv("BROWSER_USE_API_KEY")
    if not api_key:
        raise ValueError("BROWSER_USE_API_KEY environment variable is required")
    
    profile_id = os.getenv("BROWSER_USE_PROFILE_ID")
    if not profile_id:
        raise ValueError("BROWSER_USE_PROFILE_ID environment variable is required")
    
    # Initialize the client
    client = BrowserUse(api_key=api_key)
    
    print("🌐 Browser Use Demo - Google Maps Search")
    print("=" * 50)
    print(f"♻️ Using profile: {profile_id}")
    
    # Create a session with the profile
    print(f"\n📍 Creating session with profile...")
    session = client.sessions.create_session(profile_id=profile_id)
    print(f"   Session ID: {session.id}")
    
    try:
        # Create and run the task
        print(f"\n🗺️ Searching for: {address}")
        task = client.tasks.create_task(
            session_id=session.id,
            llm="browser-use-llm",
            task=f"Go to Google Maps (maps.google.com) and search for '{address}'. Wait for the results to load and then report what you find at this location."
        )
        
        print(f"   Task ID: {task.id}")
        print(f"   Status: Running...")
        
        # Wait for the task to complete
        result = task.complete()
        
        print(f"\n✅ Task completed!")
        print(f"   Final URL: {result.final_url if hasattr(result, 'final_url') else 'N/A'}")
        print(f"   Output: {result.output if hasattr(result, 'output') else result}")
        
    finally:
        # Session cleanup - profile state is preserved for next time!
        print(f"\n🛑 Session complete (profile state is preserved for next time!)")


async def main():
    """Main entry point."""
    try:
        await search_google_maps("101 Polk St")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
