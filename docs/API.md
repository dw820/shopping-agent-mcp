# Shopping Agent MCP Server API Documentation

## Overview

The Shopping Agent MCP Server provides browser automation capabilities for shopping tasks through the Model Context Protocol (MCP). This document details the API endpoints, tool specifications, and integration methods.

## MCP Protocol Compliance

The server implements the MCP specification version 1.0 and supports:

- Tool discovery and invocation
- Resource listing and reading
- Streamable HTTP transport

## Core Components

### Server Instance

The server is built using FastMCP from the `mcp` Python package:

```python
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("shopping-agent")
```

### Available Tools

#### 1. shop_product

**Tool ID**: `shop_product`

**Description**: Automates the process of searching for and purchasing a product on configured e-commerce websites using browser automation.

**Parameters Schema**:
```typescript
{
  type: "object",
  properties: {
    product_name: {
      type: "string",
      description: "Name or description of the product to search for"
    },
    max_price: {
      type: "number",
      description: "Maximum price limit for the product (optional)",
      minimum: 0
    },
    quantity: {
      type: "integer",
      description: "Quantity to purchase (default: 1)",
      minimum: 1,
      default: 1
    }
  },
  required: ["product_name"]
}
```

**Response Schema**:
```typescript
{
  type: "object",
  properties: {
    success: {
      type: "boolean",
      description: "Whether the operation was successful"
    },
    product: {
      type: "object",
      properties: {
        name: { type: "string" },
        price: { type: "number" },
        url: { type: "string", format: "uri" }
      }
    },
    order: {
      type: "object",
      properties: {
        id: { type: "string" },
        status: { type: "string" },
        estimated_delivery: { type: "string", format: "date" }
      }
    },
    message: { type: "string" },
    error: { type: "string" }
  },
  required: ["success"]
}
```

**Error Responses**:
- `400`: Invalid parameters (missing product_name, invalid price/quantity)
- `500`: Browser automation failure or internal server error

**Example Request**:
```json
{
  "product_name": "wireless gaming mouse",
  "max_price": 80,
  "quantity": 1
}
```

**Example Success Response**:
```json
{
  "success": true,
  "product": {
    "name": "Logitech G Pro Wireless Gaming Mouse",
    "price": 79.99,
    "url": "https://example.com/products/g-pro-wireless"
  },
  "order": {
    "id": "ORD-2024-001234",
    "status": "processing",
    "estimated_delivery": "2024-01-20"
  },
  "message": "Product purchased successfully"
}
```

**Example Error Response**:
```json
{
  "success": false,
  "error": "Product not found within price range",
  "message": "No products matching criteria found"
}
```

## Environment Configuration

### Required Variables

The server validates these environment variables at startup:

```python
required_vars = {
    "BROWSER_USE_API_KEY": "API key for BrowserUse service",
    "BROWSER_USE_PROFILE_ID": "Profile ID for browser automation",
    "TARGET_EMAIL": "Email for website authentication",
    "TARGET_PASSWORD": "Password for website authentication", 
    "PHONE_NUMBER": "Phone number for verification (if required)"
}
```

### Validation

The `get_env_vars()` function performs validation:
- Checks all required variables are present
- Raises `ValueError` with missing variable names
- Returns dictionary of all environment variables

## Server Lifecycle

### Startup Sequence

1. Environment variable validation
2. FastMCP server initialization
3. Tool registration
4. HTTP transport setup
5. Server ready for connections

### Shutdown

The server handles graceful shutdown on:
- SIGTERM signal
- Keyboard interrupt (Ctrl+C)
- Client disconnect

## Integration Examples

### Python Client

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    # Configure server
    server_params = StdioServerParameters(
        command="python",
        args=["src/main.py"],
        env={
            "BROWSER_USE_API_KEY": "key",
            "BROWSER_USE_PROFILE_ID": "profile",
            "TARGET_EMAIL": "email",
            "TARGET_PASSWORD": "password",
            "PHONE_NUMBER": "phone"
        }
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize connection
            await session.initialize()
            
            # List available tools
            tools = await session.list_tools()
            print(f"Available tools: {[t.name for t in tools.tools]}")
            
            # Call shop_product tool
            result = await session.call_tool(
                "shop_product",
                arguments={
                    "product_name": "laptop",
                    "max_price": 1000
                }
            )
            
            print(f"Result: {result.content}")

asyncio.run(main())
```

### Node.js Client

```javascript
const { McpServer } = require('@modelcontextprotocol/sdk');

async function connectToShoppingAgent() {
  const server = new McpServer({
    transport: {
      type: 'stdio',
      command: 'python',
      args: ['src/main.py'],
      env: {
        BROWSER_USE_API_KEY: process.env.BROWSER_USE_API_KEY,
        BROWSER_USE_PROFILE_ID: process.env.BROWSER_USE_PROFILE_ID,
        TARGET_EMAIL: process.env.TARGET_EMAIL,
        TARGET_PASSWORD: process.env.TARGET_PASSWORD,
        PHONE_NUMBER: process.env.PHONE_NUMBER
      }
    }
  });
  
  await server.connect();
  
  const tools = await server.listTools();
  console.log('Tools:', tools);
  
  const result = await server.callTool('shop_product', {
    product_name: 'smartphone',
    max_price: 500
  });
  
  console.log('Purchase result:', result);
}
```

## Testing

### Test Suite

The `tests/test_server.py` file contains comprehensive tests:

1. **Module Import Test**: Verifies server modules can be imported
2. **Server Instance Test**: Confirms mcp is a FastMCP instance
3. **Tool Registration Test**: Verifies shop_product tool is properly registered

### Running Tests

```bash
# Run all tests
python tests/test_server.py

# Expected output:
# Testing Shopping Agent MCP Server
# [OK] Server modules imported successfully
# [OK] mcp is FastMCP instance  
# [OK] shop_product tool is defined
# [SUCCESS] All tests passed! Server is ready.
```

## Error Handling

### Common Error Codes

| Code | Description | Resolution |
|------|-------------|------------|
| `ENV_VAR_MISSING` | Required environment variable not set | Set all required environment variables |
| `BROWSER_API_ERROR` | BrowserUse API communication failure | Check API key, profile ID, and network |
| `AUTH_FAILURE` | Website authentication failed | Verify credentials and website accessibility |
| `PRODUCT_NOT_FOUND` | No products matching criteria | Adjust search parameters |
| `CHECKOUT_FAILED` | Purchase process failed | Check payment method and stock availability |

### Debugging

Enable verbose logging by setting:
```bash
export LOG_LEVEL=DEBUG
```

Debug output includes:
- Browser automation steps
- Network requests and responses
- Tool execution timing
- Error stack traces

## Performance Considerations

### Timeouts

- Tool execution timeout: 300 seconds (5 minutes)
- Browser operation timeout: 60 seconds per step
- Network request timeout: 30 seconds

### Resource Usage

- Memory: ~100-200MB during browser automation
- CPU: Moderate during active automation
- Network: Varies based on website complexity

## Security

### Authentication

- All credentials passed via environment variables
- No credentials stored in code or logs
- Secure transport recommended for production

### Browser Isolation

- Each tool execution uses isolated browser context
- Cookies and sessions cleared between executions
- No persistent browser state

### Input Validation

- All tool parameters validated for type and constraints
- Price and quantity bounds enforced
- SQL injection and XSS protection in browser automation

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024-01-01 | Initial release with shop_product tool |
| 1.1.0 | 2024-01-15 | Added price filtering and quantity support |

## Support

For API-related issues:
1. Check error messages and logs
2. Verify environment configuration
3. Ensure BrowserUse service is operational
4. Contact support with error details and reproduction steps