import asyncio
from dedalus_labs import AsyncDedalus, DedalusRunner
from dotenv import load_dotenv

load_dotenv()


async def main():
    client = AsyncDedalus()
    runner = DedalusRunner(client)

    # Test prompt to shop for protein bars with shipping details
    input_prompt = """
    Please use the MCP tools to search for and purchase "protein bars".
    
    Use the following shipping information:
    - First Name: Wei
    - Last Name: Tu
    - Address: 101 Polk St
    - Unit: Unit 1113
    - City: San Francisco
    - State: CA
    - Zip Code: 94102
    """

    print("Starting Dedalus run...")

    result = await runner.run(
        input=input_prompt,
        model="openai/gpt-4o-mini",
        # Use our local MCP server
        mcp_servers=["dw820/shopping-agent-mcp"]
    )

    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
