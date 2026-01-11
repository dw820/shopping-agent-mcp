# Shopping Agent MCP Server

A Model Context Protocol (MCP) server that provides shopping automation capabilities through browser automation tools.

## Overview

This MCP server enables AI assistants to perform shopping tasks on e-commerce websites. It provides tools for product search, price comparison, and automated purchasing workflows.

## Features

- **Product Search**: Find products across multiple retailers
- **Price Comparison**: Compare prices for the same product
- **Automated Purchasing**: Complete checkout processes automatically
- **Browser Automation**: Uses Browser Use API for reliable web interactions

## Quick Start

### Prerequisites

- Python 3.8 or higher
- Browser Use API credentials
- Target website account credentials

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/shopping-agent-mcp.git
cd shopping-agent-mcp
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
export BROWSER_USE_API_KEY="your_api_key"
export BROWSER_USE_PROFILE_ID="your_profile_id"
export TARGET_EMAIL="your_email@example.com"
export TARGET_PASSWORD="your_password"
export PHONE_NUMBER="+1234567890"
```

### Running the Server

Start the MCP server:
```bash
python src/main.py
```

The server will start and be ready to accept connections via the MCP protocol.

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `BROWSER_USE_API_KEY` | API key for Browser Use service | Yes |
| `BROWSER_USE_PROFILE_ID` | Profile ID for browser sessions | Yes |
| `TARGET_EMAIL` | Email for target website login | Yes |
| `TARGET_PASSWORD` | Password for target website login | Yes |
| `PHONE_NUMBER` | Phone number for verification | Yes |

### MCP Integration

To use with Claude Desktop or other MCP clients:

1. Add to your Claude Desktop configuration (`claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "shopping-agent": {
      "command": "python",
      "args": ["/path/to/shopping-agent-mcp/src/main.py"],
      "env": {
        "BROWSER_USE_API_KEY": "your_api_key",
        "BROWSER_USE_PROFILE_ID": "your_profile_id",
        "TARGET_EMAIL": "your_email@example.com",
        "TARGET_PASSWORD": "your_password",
        "PHONE_NUMBER": "+1234567890"
      }
    }
  }
}
```

## Available Tools

### `shop_product`

Search for and purchase products on target websites.

**Parameters:**
- `product_name` (string): Name of the product to search for
- `max_price` (number, optional): Maximum price to consider
- `quantity` (number, optional): Quantity to purchase (default: 1)
- `preferred_retailer` (string, optional): Preferred retailer name

**Returns:**
- JSON object with purchase status, order details, and price information

**Example Usage:**
```python
# Through MCP client
result = await client.call_tool("shop_product", {
    "product_name": "wireless headphones",
    "max_price": 150,
    "quantity": 1,
    "preferred_retailer": "Amazon"
})
```

## API Documentation

### Main Server (`src/main.py`)

The server is built using FastMCP from the MCP Python SDK.

**Functions:**
- `main()`: Entry point that starts the MCP server
- `get_env_vars()`: Validates and retrieves required environment variables

### Tool Implementation (`src/tools/shop.py`)

Contains the `shop_product` tool implementation with browser automation logic.

## Testing

Run the test suite to verify server functionality:

```bash
python -m pytest tests/
```

Or run the manual test:

```bash
python tests/test_server.py
```

## Development

### Project Structure

```
shopping-agent-mcp/
├── src/
│   ├── main.py              # Server entry point
│   └── tools/
│       └── shop.py          # Shopping tool implementation
├── tests/
│   └── test_server.py       # Server tests
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

### Adding New Tools

1. Create a new tool function in `src/tools/`
2. Decorate with `@mcp.tool()`
3. Import and register in `src/main.py`
4. Update documentation

## Troubleshooting

### Common Issues

1. **Missing environment variables**: Ensure all required variables are set
2. **Browser Use API errors**: Verify API key and profile ID are valid
3. **Login failures**: Check target website credentials
4. **MCP connection issues**: Verify Claude Desktop configuration

### Debug Mode

Enable debug logging by setting environment variable:
```bash
export DEBUG=true
```

## Security Considerations

- Store credentials in environment variables, not in code
- Use secure password management
- Regularly rotate API keys
- Monitor for unauthorized access

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review existing GitHub issues
3. Create a new issue with detailed information