# API Documentation

## Overview

The Shopping Agent MCP Server provides a single tool for automating product shopping tasks through browser automation.

## MCP Server

### Server Initialization

The server is initialized using FastMCP from the `mcp` package:

```python
mcp = FastMCP("Shopping Agent")
```

### Transport

The server uses streamable HTTP transport for communication with MCP clients:

```python
mcp.run(transport="streamable-http")
```

## Tools

### shop_product

The primary tool for automating product shopping tasks.

#### Description
Automates the complete shopping workflow including:
1. Browser initialization and navigation
2. Product search
3. Price filtering (if specified)
4. Product selection
5. Cart management
6. Checkout process
7. Purchase confirmation

#### Parameters

| Parameter | Type | Required | Description | Default |
|-----------|------|----------|-------------|---------|
| `product_name` | string | Yes | Name of the product to search for | - |
| `max_price` | number | No | Maximum price limit for the product | None |
| `quantity` | number | No | Quantity to purchase | 1 |

#### Return Value

Returns a JSON object with the following structure:

```json
{
  "success": boolean,
  "message": string,
  "product": string,
  "price": number,
  "quantity": number,
  "timestamp": string
}
```

#### Example Request

```json
{
  "product_name": "wireless headphones",
  "max_price": 200,
  "quantity": 1
}
```

#### Example Response

```json
{
  "success": true,
  "message": "Successfully purchased wireless headphones",
  "product": "Sony WH-1000XM4 Wireless Headphones",
  "price": 179.99,
  "quantity": 1,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### Error Responses

| Error Type | HTTP Status | Description |
|------------|-------------|-------------|
| Validation Error | 400 | Invalid parameters or missing required fields |
| Authentication Error | 401 | BrowserUse API authentication failed |
| Browser Error | 500 | Browser automation failed |
| Purchase Error | 500 | Checkout or payment process failed |

## Environment Variables

### Required Variables

All environment variables are validated at server startup via the `get_env_vars()` function.

#### `BROWSER_USE_API_KEY`
- **Type**: String
- **Purpose**: Authentication key for BrowserUse API
- **Format**: UUID or API key string
- **Validation**: Non-empty string

#### `BROWSER_USE_PROFILE_ID`
- **Type**: String
- **Purpose**: Identifier for browser profile configuration
- **Format**: Profile identifier string
- **Validation**: Non-empty string

#### `TARGET_EMAIL`
- **Type**: String
- **Purpose**: Email address for target website authentication
- **Format**: Valid email address
- **Validation**: Non-empty string, basic email format validation

#### `TARGET_PASSWORD`
- **Type**: String
- **Purpose**: Password for target website authentication
- **Format**: Password string
- **Validation**: Non-empty string

#### `PHONE_NUMBER`
- **Type**: String
- **Purpose**: Phone number for verification (if required)
- **Format**: Phone number in any format
- **Validation**: Non-empty string

### Validation Process

The `get_env_vars()` function:
1. Retrieves all required environment variables
2. Checks each variable is not `None` or empty
3. Raises `ValueError` with list of missing variables if any are missing
4. Returns dictionary of all variables if validation passes

## Testing

### Test Suite

The test suite in `tests/test_server.py` validates:

1. **Module Import**: Server modules can be imported successfully
2. **Server Instance**: `mcp` is a valid `FastMCP` instance
3. **Tool Registration**: `shop_product` tool is properly defined

### Running Tests

```bash
python tests/test_server.py
```

### Test Output

Successful test output includes:
- Import status
- Server instance validation
- Tool registration check
- Summary of all tests passed

## Integration

### MCP Client Integration

Clients can integrate with the server using standard MCP protocols:

```python
# Example client integration
async with mcp_client as client:
    result = await client.call_tool("shop_product", {
        "product_name": "product name",
        "max_price": 100
    })
```

### Error Handling

The server provides structured error responses:

```python
try:
    result = await client.call_tool("shop_product", params)
except MCPError as e:
    print(f"Tool execution failed: {e.message}")
```

## Security Considerations

1. **Environment Variables**: Sensitive data stored in `.env` file, excluded from version control
2. **API Keys**: BrowserUse API key should be rotated regularly
3. **Credentials**: Target website credentials should use dedicated accounts
4. **Validation**: All input parameters are validated before processing

## Performance

- **Browser Automation**: Operations may take several seconds depending on website responsiveness
- **Concurrency**: Single tool execution at a time (consider rate limiting for production)
- **Resource Usage**: Browser automation may consume significant memory

## Monitoring

Recommended monitoring metrics:
- Tool execution success rate
- Average execution time
- Browser automation failures
- Environment variable validation failures