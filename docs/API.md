# Shopping Agent MCP Server API Documentation

## Table of Contents

1. [Overview](#overview)
2. [Server Architecture](#server-architecture)
3. [Tool API](#tool-api)
4. [Environment Variables](#environment-variables)
5. [Error Handling](#error-handling)
6. [Examples](#examples)

## Overview

The Shopping Agent MCP Server provides a standardized interface for shopping automation through the Model Context Protocol (MCP). It enables AI assistants to perform complex shopping tasks with minimal configuration.

## Server Architecture

### Core Components

#### Main Server (`src/main.py`)

The main server file initializes the MCP server and registers available tools.

**Key Functions:**

```python
def main() -> None:
    """Start the MCP server."""
    # Server initialization and startup

def get_env_vars() -> dict:
    """Get required environment variables."""
    # Validates and returns environment configuration
```

#### Tool Registration

Tools are registered using the FastMCP decorator pattern:

```python
@mcp.tool()
async def shop_product(
    product_name: str,
    max_price: Optional[float] = None,
    quantity: int = 1,
    preferred_retailer: Optional[str] = None
) -> dict:
    """Search for and purchase products."""
```

### MCP Protocol Compliance

The server implements the MCP specification for:
- Tool definition and invocation
- Resource management
- Prompt templates
- Error reporting

## Tool API

### `shop_product` Tool

#### Description
Searches for products across configured retailers, compares prices, and completes purchases when criteria are met.

#### Parameters

| Parameter | Type | Required | Description | Default |
|-----------|------|----------|-------------|---------|
| `product_name` | string | Yes | Name or description of product to search for | - |
| `max_price` | number | No | Maximum acceptable price | None |
| `quantity` | integer | No | Number of units to purchase | 1 |
| `preferred_retailer` | string | No | Preferred retailer for purchase | None |

#### Return Value

Returns a JSON object with the following structure:

```json
{
  "success": boolean,
  "message": string,
  "order_id": string | null,
  "product_found": boolean,
  "price": number | null,
  "retailer": string | null,
  "timestamp": string,
  "errors": array | null
}
```

#### Field Descriptions

- `success`: Whether the operation completed successfully
- `message`: Human-readable status message
- `order_id`: Unique identifier for the purchase order (if successful)
- `product_found`: Whether the product was found at any retailer
- `price`: Final purchase price (if successful)
- `retailer`: Retailer where purchase was made
- `timestamp`: ISO 8601 timestamp of operation completion
- `errors`: Array of error messages if operation failed

#### Error Conditions

The tool may return errors in the following cases:

1. **Product not found**: No matching products at any configured retailer
2. **Price exceeds limit**: All found products exceed `max_price` parameter
3. **Authentication failure**: Cannot log into target website
4. **Browser error**: Browser automation service unavailable
5. **Checkout failure**: Payment or shipping information rejected

## Environment Variables

### Required Variables

#### `BROWSER_USE_API_KEY`
- **Type**: String
- **Purpose**: Authentication key for Browser Use API
- **Format**: UUID or API key string
- **Security**: Highly sensitive - store in secure environment

#### `BROWSER_USE_PROFILE_ID`
- **Type**: String
- **Purpose**: Identifier for browser profile configuration
- **Format**: Profile identifier string
- **Notes**: Defines browser settings and capabilities

#### `TARGET_EMAIL`
- **Type**: String
- **Purpose**: Email address for target website authentication
- **Format**: Valid email address
- **Security**: Store securely, consider using app-specific credentials

#### `TARGET_PASSWORD`
- **Type**: String
- **Purpose**: Password for target website authentication
- **Format**: Password string
- **Security**: Highly sensitive - never commit to version control

#### `PHONE_NUMBER`
- **Type**: String
- **Purpose**: Phone number for two-factor authentication
- **Format**: E.164 format (e.g., +1234567890)
- **Notes**: Required for websites with SMS verification

### Optional Variables

#### `DEBUG`
- **Type**: Boolean
- **Purpose**: Enable debug logging
- **Default**: `false`
- **Values**: `true` or `false`

#### `LOG_LEVEL`
- **Type**: String
- **Purpose**: Control logging verbosity
- **Default**: `INFO`
- **Values**: `DEBUG`, `INFO`, `WARNING`, `ERROR`

#### `TIMEOUT_SECONDS`
- **Type**: Integer
- **Purpose**: Operation timeout in seconds
- **Default**: `300` (5 minutes)

## Error Handling

### Error Types

#### Configuration Errors
Occur during server startup when environment variables are missing or invalid.

**Example:**
```json
{
  "error": "ConfigurationError",
  "message": "Missing required environment variables: BROWSER_USE_API_KEY, TARGET_EMAIL",
  "details": {
    "missing_vars": ["BROWSER_USE_API_KEY", "TARGET_EMAIL"]
  }
}
```

#### Tool Execution Errors
Occur during tool execution when operations fail.

**Example:**
```json
{
  "error": "ToolExecutionError",
  "message": "Failed to complete purchase: Payment declined",
  "tool": "shop_product",
  "parameters": {
    "product_name": "wireless headphones",
    "max_price": 150
  }
}
```

#### Browser Automation Errors
Occur when browser automation service fails.

**Example:**
```json
{
  "error": "BrowserError",
  "message": "Browser Use API unavailable",
  "service": "browser-use",
  "status_code": 503
}
```

### Error Recovery

The server implements the following recovery strategies:

1. **Retry logic**: Automatic retries for transient failures
2. **Fallback retailers**: Try alternative retailers if primary fails
3. **Session recovery**: Re-establish browser sessions on failure
4. **Timeout handling**: Graceful timeout with cleanup

## Examples

### Basic Product Search

```python
# Search for a product without purchasing
result = await client.call_tool("shop_product", {
    "product_name": "coffee maker",
    "max_price": 100
})

if result["product_found"]:
    print(f"Found product at ${result['price']}")
else:
    print("Product not found within price range")
```

### Complete Purchase

```python
# Purchase a specific product
result = await client.call_tool("shop_product", {
    "product_name": "iPhone 15 case",
    "max_price": 25,
    "quantity": 2,
    "preferred_retailer": "Amazon"
})

if result["success"]:
    print(f"Purchase successful! Order ID: {result['order_id']}")
else:
    print(f"Purchase failed: {result['message']}")
```

### Error Handling Example

```python
try:
    result = await client.call_tool("shop_product", {
        "product_name": "gaming laptop",
        "max_price": 2000
    })
    
    if "errors" in result and result["errors"]:
        for error in result["errors"]:
            print(f"Error: {error}")
    else:
        print(f"Success: {result['message']}")
        
except Exception as e:
    print(f"Tool invocation failed: {e}")
```

### Integration with Claude Desktop

```json
{
  "mcpServers": {
    "shopping-agent": {
      "command": "python",
      "args": ["/absolute/path/to/src/main.py"],
      "env": {
        "BROWSER_USE_API_KEY": "sk-...",
        "BROWSER_USE_PROFILE_ID": "profile-123",
        "TARGET_EMAIL": "user@example.com",
        "TARGET_PASSWORD": "secure_password",
        "PHONE_NUMBER": "+1234567890",
        "DEBUG": "false",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

## Best Practices

### Security
1. Use environment variables for all credentials
2. Implement credential rotation policies
3. Monitor for unauthorized access attempts
4. Use secure communication channels

### Performance
1. Set appropriate timeouts for operations
2. Implement caching where appropriate
3. Monitor browser session usage
4. Clean up resources after operations

### Reliability
1. Implement comprehensive error handling
2. Add retry logic for transient failures
3. Monitor service health
4. Maintain audit logs of all operations

## Version History

- **v1.0.0**: Initial release with basic shopping functionality
- **v1.1.0**: Added error recovery and improved logging
- **v1.2.0**: Multi-retailer support and price comparison

## Support

For API-related questions or issues:
1. Check the [README.md](../README.md) for basic setup
2. Review existing GitHub issues
3. Contact support with detailed error information