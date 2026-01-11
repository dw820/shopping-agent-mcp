# Shopping Agent MCP Server

A Model Context Protocol (MCP) server that provides shopping automation capabilities through browser automation tools.

## Features

- **Product Shopping Tool**: Automate product searches and purchases on e-commerce websites
- **Browser Automation**: Uses BrowserUse API for reliable web automation
- **Environment Configuration**: Secure configuration through environment variables
- **FastMCP Integration**: Built on the FastMCP framework for MCP compatibility

## Prerequisites

- Python 3.8 or higher
- BrowserUse API key and profile ID
- Target website credentials (email, password, phone number)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd shopping-agent-mcp
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables (see Configuration section below)

## Configuration

The server requires the following environment variables:

| Variable | Description | Required |
|----------|-------------|----------|
| `BROWSER_USE_API_KEY` | API key for BrowserUse service | Yes |
| `BROWSER_USE_PROFILE_ID` | Profile ID for BrowserUse | Yes |
| `TARGET_EMAIL` | Email for target website login | Yes |
| `TARGET_PASSWORD` | Password for target website login | Yes |
| `PHONE_NUMBER` | Phone number for verification (if needed) | Yes |

### Setting Environment Variables

#### Linux/macOS:
```bash
export BROWSER_USE_API_KEY="your-api-key"
export BROWSER_USE_PROFILE_ID="your-profile-id"
export TARGET_EMAIL="your-email@example.com"
export TARGET_PASSWORD="your-password"
export PHONE_NUMBER="+1234567890"
```

#### Windows (PowerShell):
```powershell
$env:BROWSER_USE_API_KEY="your-api-key"
$env:BROWSER_USE_PROFILE_ID="your-profile-id"
$env:TARGET_EMAIL="your-email@example.com"
$env:TARGET_PASSWORD="your-password"
$env:PHONE_NUMBER="+1234567890"
```

#### Using .env file:
Create a `.env` file in the project root:
```env
BROWSER_USE_API_KEY=your-api-key
BROWSER_USE_PROFILE_ID=your-profile-id
TARGET_EMAIL=your-email@example.com
TARGET_PASSWORD=your-password
PHONE_NUMBER=+1234567890
```

## Usage

### Starting the Server

Run the server with:
```bash
python src/main.py
```

The server will start and display available tools:
```
🛒 Starting Shopping Agent MCP Server...
🔧 Available tools: shop_product
```

### Available Tools

#### `shop_product` Tool

**Description**: Searches for and purchases a product on configured e-commerce websites.

**Parameters**:
- `product_name` (string, required): Name of the product to search for
- `max_price` (number, optional): Maximum price limit for the product
- `quantity` (integer, optional): Quantity to purchase (default: 1)

**Returns**:
- JSON object with purchase status, product details, and order information

**Example Usage**:
```python
# Through MCP client
result = await client.call_tool("shop_product", {
    "product_name": "wireless headphones",
    "max_price": 150,
    "quantity": 2
})
```

### Integration with Claude Desktop

To use this server with Claude Desktop:

1. Add the server configuration to your Claude Desktop config file (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "shopping-agent": {
      "command": "python",
      "args": ["/path/to/shopping-agent-mcp/src/main.py"],
      "env": {
        "BROWSER_USE_API_KEY": "your-api-key",
        "BROWSER_USE_PROFILE_ID": "your-profile-id",
        "TARGET_EMAIL": "your-email@example.com",
        "TARGET_PASSWORD": "your-password",
        "PHONE_NUMBER": "+1234567890"
      }
    }
  }
}
```

2. Restart Claude Desktop

3. The shopping tools will be available in your Claude conversations

## API Documentation

### Server Endpoints

The server exposes the following MCP endpoints:

- `/tools/list` - List available tools
- `/tools/call` - Call a specific tool
- `/resources/list` - List available resources
- `/resources/read` - Read a specific resource

### Tool Response Format

The `shop_product` tool returns responses in the following format:

```json
{
  "success": true,
  "product": {
    "name": "Product Name",
    "price": 99.99,
    "url": "https://example.com/product"
  },
  "order": {
    "id": "ORDER12345",
    "status": "confirmed",
    "estimated_delivery": "2024-01-15"
  },
  "message": "Product purchased successfully"
}
```

## Testing

Run the test suite to verify server functionality:

```bash
python tests/test_server.py
```

Expected output:
```
Testing Shopping Agent MCP Server

[OK] Server modules imported successfully

Test 1: Server instance...
[OK] mcp is FastMCP instance

Test 2: Tool registration...
[OK] shop_product tool is defined

==================================================
[SUCCESS] All tests passed! Server is ready.
```

## Troubleshooting

### Common Issues

1. **Missing environment variables**:
   ```
   ValueError: Missing required environment variables: BROWSER_USE_API_KEY, TARGET_EMAIL
   ```
   **Solution**: Ensure all required environment variables are set.

2. **Import errors**:
   ```
   ImportError: No module named 'mcp'
   ```
   **Solution**: Install all dependencies with `pip install -r requirements.txt`

3. **BrowserUse API errors**:
   ```
   BrowserUseError: Invalid API key or profile ID
   ```
   **Solution**: Verify your BrowserUse credentials are correct and the service is accessible.

### Debug Mode

For detailed logging, you can enable debug mode by setting:
```bash
export DEBUG=true
```

## Security Considerations

1. **Credentials Security**:
   - Never commit `.env` files or hardcode credentials
   - Use environment variables or secure credential managers
   - Rotate API keys regularly

2. **Browser Automation**:
   - The server performs automated browser actions
   - Ensure you have permission to automate the target websites
   - Respect website terms of service

3. **Data Privacy**:
   - Personal information (email, phone) is used only for authentication
   - No data is stored permanently by the server

## Development

### Project Structure

```
shopping-agent-mcp/
├── src/
│   └── main.py              # Main server implementation
├── tests/
│   └── test_server.py       # Test suite
├── requirements.txt         # Python dependencies
└── README.md               # This documentation
```

### Adding New Tools

To add a new tool to the server:

1. Define the tool function in `src/main.py`
2. Decorate it with `@mcp.tool()`
3. Update the documentation in this README

Example:
```python
@mcp.tool()
def new_tool(param1: str, param2: int) -> dict:
    """Description of the new tool."""
    # Implementation
    return {"result": "success"}
```

## License

[Add license information here]

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the MCP documentation
3. Open an issue in the repository