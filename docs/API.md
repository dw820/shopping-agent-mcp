# Shopping Agent MCP Server API Documentation

## Overview

The Shopping Agent MCP Server provides tools for automating shopping tasks through the Model Context Protocol (MCP). This document details the available tools, their parameters, return values, and usage examples.

## MCP Protocol Support

The server implements the MCP specification and supports:

- **Tools**: Function calls that can be invoked by clients
- **Prompts**: Template prompts for common shopping tasks
- **Resources**: Data resources available to clients

## Tools Reference

### Core Shopping Tool

#### `shop_product`

The primary tool for automating product purchases.

**Description:**
Searches for a product on specified e-commerce websites, selects the best match based on price and availability, and completes the purchase process.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `product_name` | string | Yes | - | Name or description of the product to search for |
| `max_price` | number | No | None | Maximum acceptable price for the product |
| `quantity` | integer | No | 1 | Number of units to purchase |
| `website` | string | No | "amazon" | Target e-commerce website (supported: "amazon", "walmart", "bestbuy") |
| `shipping_speed` | string | No | "standard" | Shipping preference ("standard", "expedited", "next_day") |

**Return Value:**
```json
{
  "success": boolean,
  "order_id": string,
  "product_name": string,
  "price": number,
  "quantity": number,
  "estimated_delivery": string,
  "status": string,
  "error_message": string | null
}
```

**Example Request:**
```json
{
  "product_name": "Apple AirPods Pro",
  "max_price": 249.99,
  "quantity": 1,
  "website": "amazon",
  "shipping_speed": "expedited"
}
```

**Example Response:**
```json
{
  "success": true,
  "order_id": "ORDER-123456",
  "product_name": "Apple AirPods Pro (2nd Generation)",
  "price": 229.99,
  "quantity": 1,
  "estimated_delivery": "2024-01-15",
  "status": "confirmed",
  "error_message": null
}
```

**Error Responses:**
- `{"success": false, "error_message": "Product not found within price range"}`
- `{"success": false, "error_message": "Authentication failed for target website"}`
- `{"success": false, "error_message": "Insufficient stock available"}`

## Prompts

### Available Prompts

#### `shopping_assistant`

A prompt template for AI assistants to help with shopping decisions.

**Parameters:**
- `user_query`: The user's shopping request
- `budget`: Optional budget constraint
- `preferences`: Optional user preferences

**Example Usage:**
```python
prompt = await client.get_prompt("shopping_assistant", {
    "user_query": "I need a new laptop for programming",
    "budget": 1500,
    "preferences": "lightweight, good battery life"
})
```

#### `product_comparison`

Prompt for comparing multiple products.

**Parameters:**
- `products`: List of product names to compare
- `criteria`: Comparison criteria (price, features, reviews, etc.)

## Resources

### `supported_websites`

List of supported e-commerce websites and their capabilities.

**Content:**
```json
{
  "websites": [
    {
      "name": "amazon",
      "supports": ["search", "purchase", "reviews", "prime"],
      "currency": "USD",
      "regions": ["US", "CA", "UK", "DE"]
    },
    {
      "name": "walmart",
      "supports": ["search", "purchase", "in_store_pickup"],
      "currency": "USD",
      "regions": ["US"]
    }
  ]
}
```

### `shipping_options`

Available shipping options and their characteristics.

## HTTP API Endpoints

When running in HTTP mode, the server exposes these endpoints:

### `POST /tools/call`

Call a tool by name.

**Request:**
```json
{
  "name": "shop_product",
  "arguments": {
    "product_name": "wireless mouse",
    "max_price": 50
  }
}
```

**Response:**
```json
{
  "content": [
    {
      "type": "text",
      "text": "{\"success\": true, \"order_id\": \"ORDER-789\", ...}"
    }
  ]
}
```

### `GET /tools/list`

List all available tools.

**Response:**
```json
{
  "tools": [
    {
      "name": "shop_product",
      "description": "Searches for and purchases a product",
      "inputSchema": {
        "type": "object",
        "properties": {
          "product_name": {"type": "string"},
          "max_price": {"type": "number"},
          "quantity": {"type": "integer"},
          "website": {"type": "string"}
        },
        "required": ["product_name"]
      }
    }
  ]
}
```

### `GET /health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-10T12:00:00Z",
  "version": "1.0.0"
}
```

## Authentication

### Environment-Based Authentication

The server uses environment variables for authentication:

1. **BrowserUse API**: For browser automation
2. **Website Credentials**: For target e-commerce sites

### API Key Security

- API keys are read from environment variables
- Never transmitted in API requests
- Rotated automatically based on configuration

## Rate Limiting

The server implements rate limiting to prevent abuse:

- **Default**: 100 requests per minute per client
- **Burst**: 10 requests per second
- **Tool-specific limits**: Shopping tools may have additional limits

## Error Handling

### Common Error Codes

| HTTP Status | Error Code | Description |
|-------------|------------|-------------|
| 400 | `INVALID_PARAMETERS` | Missing or invalid tool parameters |
| 401 | `AUTHENTICATION_FAILED` | BrowserUse or website authentication failed |
| 404 | `TOOL_NOT_FOUND` | Requested tool does not exist |
| 429 | `RATE_LIMITED` | Rate limit exceeded |
| 500 | `INTERNAL_ERROR` | Server internal error |

### Error Response Format

```json
{
  "error": {
    "code": "AUTHENTICATION_FAILED",
    "message": "Failed to authenticate with target website",
    "details": {
      "website": "amazon",
      "timestamp": "2024-01-10T12:00:00Z"
    }
  }
}
```

## Client Libraries

### Python Client Example

```python
import asyncio
from mcp import Client

async def shop_example():
    async with Client("http://localhost:8000") as client:
        # List available tools
        tools = await client.list_tools()
        print(f"Available tools: {[t.name for t in tools]}")

        # Call shopping tool
        result = await client.call_tool("shop_product", {
            "product_name": "gaming keyboard",
            "max_price": 100,
            "website": "amazon"
        })
        
        print(f"Purchase result: {result}")

asyncio.run(shop_example())
```

### JavaScript/TypeScript Client Example

```javascript
import { McpClient } from '@modelcontextprotocol/sdk';

async function shopProduct() {
  const client = new McpClient({
    transport: {
      type: 'http',
      url: 'http://localhost:8000'
    }
  });

  await client.connect();
  
  const result = await client.callTool({
    name: 'shop_product',
    arguments: {
      product_name: 'wireless earbuds',
      max_price: 150
    }
  });
  
  console.log('Purchase completed:', result);
  
  await client.close();
}
```

## Best Practices

### Tool Usage

1. **Validate inputs client-side** before calling tools
2. **Handle errors gracefully** with appropriate user feedback
3. **Use appropriate timeouts** for long-running operations
4. **Cache results** when appropriate to reduce API calls

### Performance

1. **Batch operations** when possible
2. **Use async/await** for non-blocking operations
3. **Monitor rate limits** to avoid throttling
4. **Implement retry logic** for transient failures

## Versioning

API versioning follows semantic versioning:

- **Major version**: Breaking changes
- **Minor version**: New features, backward compatible
- **Patch version**: Bug fixes, backward compatible

Current API version: `1.0.0`

## Changelog

### v1.0.0 (Current)
- Initial release with `shop_product` tool
- Basic MCP protocol support
- HTTP transport implementation
- Environment-based configuration