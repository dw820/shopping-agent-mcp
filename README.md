# Shopping Agent MCP Server

A Model Context Protocol (MCP) server that provides shopping automation capabilities through AI agents.

## Features

- **Product Shopping Tool**: Automatically search and purchase products online
- **Browser Automation**: Uses browser automation for seamless shopping experiences
- **Environment Configuration**: Secure configuration through environment variables
- **FastMCP Integration**: Built on the FastMCP framework for high-performance MCP servers

## Prerequisites

- Python 3.8 or higher
- Browser automation dependencies
- Required API keys and credentials

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

Create a `.env` file in the project root with the following variables:

```env
# Browser automation credentials
BROWSER_USE_API_KEY=your_browser_use_api_key
BROWSER_USE_PROFILE_ID=your_browser_use_profile_id

# Target website credentials
TARGET_EMAIL=your_email@example.com
TARGET_PASSWORD=your_password
PHONE_NUMBER=your_phone_number
```

### Environment Variables Explained

- **BROWSER_USE_API_KEY**: API key for browser automation service
- **BROWSER_USE_PROFILE_ID**: Profile ID for browser automation
- **TARGET_EMAIL**: Email for the target shopping website login
- **TARGET_PASSWORD**: Password for the target shopping website login
- **PHONE_NUMBER**: Phone number for verification (if required)

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

#### shop_product
Searches for and purchases a specified product.

**Parameters:**
- `product_name` (string): Name of the product to search for
- `max_price` (optional, number): Maximum price limit for the product
- `quantity` (optional, number): Quantity to purchase (default: 1)

**Example usage through MCP client:**
```python
# This is how an MCP client would call the tool
result = await client.call_tool("shop_product", {
    "product_name": "wireless headphones",
    "max_price": 150,
    "quantity": 2
})
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

## Development

### Project Structure

```
shopping-agent-mcp/
├── src/
│   └── main.py          # Main server implementation
├── tests/
│   └── test_server.py    # Server tests
├── requirements.txt      # Python dependencies
├── .env.example          # Example environment variables
└── README.md            # This file
```

### Adding New Tools

To add a new tool to the MCP server:

1. Define the tool function in `src/main.py` with appropriate parameters
2. Decorate it with `@mcp.tool()`
3. Update the startup message in the `main()` function
4. Add corresponding tests in `tests/test_server.py`

## Troubleshooting

### Common Issues

1. **Missing environment variables**
   - Error: `ValueError: Missing required environment variables: ...`
   - Solution: Ensure all required variables are set in your `.env` file

2. **Import errors**
   - Error: `ImportError: cannot import name 'mcp'`
   - Solution: Check that you're running from the correct directory and all dependencies are installed

3. **Browser automation failures**
   - Issue: Tool fails to interact with browser
   - Solution: Verify BROWSER_USE_API_KEY and BROWSER_USE_PROFILE_ID are valid

### Debug Mode

For detailed logging, you can modify the server startup:

```python
# In src/main.py, add logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Security Considerations

- Never commit your `.env` file to version control
- Use strong, unique passwords for TARGET_PASSWORD
- Regularly rotate API keys
- Consider using a password manager for credential storage

## License

[Add your license information here]

## Support

For issues and feature requests, please:
1. Check the troubleshooting section above
2. Review the existing GitHub issues
3. Create a new issue with detailed reproduction steps