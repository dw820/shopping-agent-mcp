# Shopping Agent MCP Server API Documentation

## Table of Contents

1. [Introduction](#introduction)
2. [Server Configuration](#server-configuration)
3. [Available Tools](#available-tools)
4. [Tool Usage Examples](#tool-usage-examples)
5. [Error Handling](#error-handling)
6. [Client Integration](#client-integration)
7. [Advanced Usage](#advanced-usage)

## Introduction

The Shopping Agent MCP Server implements the Model Context Protocol (MCP) to provide shopping automation capabilities. This document details the API interface, tool specifications, and integration guidelines.

## Server Configuration

### Server Initialization

The server is initialized in `src/main.py` and provides the following configuration options:

```python
from mcp.server.fastmcp import FastMCP

# Server instance with name and version
mcp = FastMCP("shopping-agent", version="1.0.0")
```

### Environment Variables

The server requires these environment variables to function:

```python
# src/main.py - get_env_vars() function
required_vars = {
    "BROWSER_USE_API_KEY": "API key for Browser.use service",
    "BROWSER_USE_PROFILE_ID": "Profile ID for browser automation",
    "TARGET_EMAIL": "Email for e-commerce site login",
    "TARGET_PASSWORD": "Password for e-commerce site login",
    "PHONE_NUMBER": "Phone number for verification"
}
```

### Server Endpoints

When running, the server exposes:

- **MCP-over-HTTP**: Primary protocol endpoint (default: `http://localhost:8000`)
- **Health Check**: `GET /health` - Returns server status
- **Tools List**: `GET /tools` - Returns registered tools metadata

## Available Tools

### shop_product

The primary tool for searching and purchasing products.

#### Tool Signature

```python
@mcp.tool()
def shop_product(
    product_name: str,
    max_price: float | None = None,
    retailer: str = "amazon",
    quantity: int = 1
) -> dict:
```

#### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `product_name` | string | Yes | - | Name or description of product to search |
| `max_price` | number | No | None | Maximum price in USD. If not specified, no price limit |
| `retailer` | string | No | "amazon" | Retailer to search. Supported: "amazon", "bestbuy", "walmart" |
| `quantity` | integer | No | 1 | Number of items to purchase |

#### Return Value

Returns a dictionary with the following structure:

```json
{
    "success": true,
    "order_id": "ORD-123456789",
    "product_name": "Product Name",
    "price": 99.99,
    "currency": "USD",
    "retailer": "amazon",
    "quantity": 1,
    "estimated_delivery": "2024-12-25",
    "purchase_timestamp": "2024-12-20T10:30:00Z",
    "shipping_address": {
        "name": "John Doe",
        "street": "123 Main St",
        "city": "Anytown",
        "state": "CA",
        "zip": "12345",
        "country": "USA"
    }
}
```

#### Error Responses

If the tool fails, it returns:

```json
{
    "success": false,
    "error": "Error description",
    "error_code": "ERROR_TYPE",
    "suggestion": "Optional suggestion for resolution"
}
```

Common error codes:
- `AUTHENTICATION_FAILED`: Login credentials invalid
- `PRODUCT_NOT_FOUND`: No matching products found
- `PRICE_EXCEEDS_LIMIT`: All products exceed max_price
- `CHECKOUT_FAILED`: Payment or checkout process failed
- `NETWORK_ERROR`: Connection issues with retailer site

## Tool Usage Examples

### Basic Product Search

```python
# Search for headphones on Amazon
result = await client.call_tool("shop_product", {
    "product_name": "wireless noise-cancelling headphones"
})

if result["success"]:
    print(f"Purchased {result['product_name']} for ${result['price']}")
    print(f"Order ID: {result['order_id']}")
else:
    print(f"Failed: {result['error']}")
```

### Price-Limited Search

```python
# Find a laptop under $1000 at Best Buy
result = await client.call_tool("shop_product", {
    "product_name": "gaming laptop",
    "max_price": 1000,
    "retailer": "bestbuy"
})
```

### Bulk Purchase

```python
# Buy 3 units of a product
result = await client.call_tool("shop_product", {
    "product_name": "AA batteries",
    "retailer": "walmart",
    "quantity": 3
})
```

## Error Handling

### Common Error Scenarios

1. **Invalid Credentials**
   ```json
   {
       "success": false,
       "error": "Login failed with provided credentials",
       "error_code": "AUTHENTICATION_FAILED",
       "suggestion": "Check TARGET_EMAIL and TARGET_PASSWORD environment variables"
   }
   ```

2. **Product Not Available**
   ```json
   {
       "success": false,
       "error": "No products found matching 'out of stock product'",
       "error_code": "PRODUCT_NOT_FOUND",
       "suggestion": "Try a different search term or retailer"
   }
   ```

3. **Price Limit Exceeded**
   ```json
   {
       "success": false,
       "error": "All found products exceed $50 limit",
       "error_code": "PRICE_EXCEEDS_LIMIT",
       "suggestion": "Increase max_price or search for different product"
   }
   ```

### Retry Logic

For transient errors (network issues, temporary outages), implement retry logic in your client:

```python
import asyncio
from typing import Optional

async def call_with_retry(tool_name: str, params: dict, max_retries: int = 3) -> Optional[dict]:
    for attempt in range(max_retries):
        try:
            result = await client.call_tool(tool_name, params)
            if result["success"]:
                return result
            elif result["error_code"] in ["NETWORK_ERROR", "TIMEOUT"]:
                # Retry on network errors
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
                continue
            else:
                # Non-retryable error
                return result
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(2 ** attempt)
    return None
```

## Client Integration

### Python Client Example

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    # Configure server connection
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "src.main"],
        env={
            "BROWSER_USE_API_KEY": "your_key",
            "BROWSER_USE_PROFILE_ID": "your_profile",
            "TARGET_EMAIL": "email@example.com",
            "TARGET_PASSWORD": "password",
            "PHONE_NUMBER": "+1234567890"
        }
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize session
            await session.initialize()
            
            # List available tools
            tools = await session.list_tools()
            print(f"Available tools: {[t.name for t in tools.tools]}")
            
            # Call shop_product tool
            result = await session.call_tool(
                "shop_product",
                arguments={
                    "product_name": "coffee maker",
                    "max_price": 80,
                    "retailer": "amazon"
                }
            )
            
            print(f"Result: {result.content}")
            
if __name__ == "__main__":
    asyncio.run(main())
```

### JavaScript/TypeScript Client Example

```typescript
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';

async function runShoppingAgent() {
    const transport = new StdioClientTransport({
        command: 'python',
        args: ['-m', 'src.main']
    });
    
    const client = new Client(
        { name: 'shopping-client', version: '1.0.0' },
        { capabilities: {} }
    );
    
    await client.connect(transport);
    
    // List tools
    const tools = await client.listTools();
    console.log('Tools:', tools.tools);
    
    // Call shop_product
    const result = await client.callTool({
        name: 'shop_product',
        arguments: {
            product_name: 'wireless mouse',
            max_price: 50,
            retailer: 'bestbuy'
        }
    });
    
    console.log('Purchase result:', result.content);
    
    await client.close();
}

runShoppingAgent().catch(console.error);
```

## Advanced Usage

### Custom Tool Development

To add custom tools to the server:

1. Create a new tool module in `src/tools/`:

```python
# src/tools/custom_tools.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("custom-tools")

@mcp.tool()
async def compare_prices(product_name: str, retailers: list[str]) -> dict:
    """Compare prices across multiple retailers."""
    # Implementation
    return {
        "product": product_name,
        "comparisons": [
            {"retailer": "amazon", "price": 99.99},
            {"retailer": "walmart", "price": 89.99}
        ]
    }
```

2. Import and register in `src/main.py`:

```python
# Add to src/main.py
from src.tools.custom_tools import mcp as custom_mcp

# The tools will be automatically registered
```

### Performance Optimization

For high-volume usage:

1. **Connection Pooling**: Reuse browser sessions
2. **Caching**: Cache product search results
3. **Async Operations**: Use async/await for I/O operations
4. **Rate Limiting**: Respect retailer API rate limits

### Monitoring and Logging

Enable detailed logging for debugging:

```bash
# Set log level
export LOG_LEVEL=DEBUG

# Start server with verbose output
python -m src.main --verbose
```

Logs include:
- Tool execution times
- Browser automation steps
- Network requests and responses
- Error details and stack traces

## Testing

Refer to `tests/test_server.py` for API testing examples:

```python
def test_server():
    """Test all server functionality."""
    # Import and verify server components
    from src.main import mcp, shop_product
    
    # Verify FastMCP instance
    from mcp.server.fastmcp import FastMCP
    assert isinstance(mcp, FastMCP)
    
    # Verify tool registration
    assert shop_product is not None
    
    print("[SUCCESS] All tests passed! Server is ready.")
```

## Support

For API issues or questions:
1. Check the [GitHub Issues](https://github.com/yourusername/shopping-agent-mcp/issues)
2. Review the [MCP Documentation](https://modelcontextprotocol.io)
3. Enable debug logging for detailed error information