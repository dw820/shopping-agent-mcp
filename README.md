# Shopping Agent MCP Server

An MCP (Model Context Protocol) server that provides shopping automation capabilities through browser automation tools.

## Features

- **Product Shopping Tool**: Automates product search and purchase workflows
- **Browser Automation**: Uses BrowserUse API for reliable browser interactions
- **Environment-based Configuration**: Secure credential management
- **FastMCP Server**: High-performance MCP server implementation

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

3. Set up environment variables:
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your actual credentials
nano .env  # or use your preferred editor
```

## Configuration

### Required Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# BrowserUse API credentials
BROWSER_USE_API_KEY=your_browseruse_api_key_here
BROWSER_USE_PROFILE_ID=your_profile_id_here

# Target website credentials
TARGET_EMAIL=your_email@example.com
TARGET_PASSWORD=your_password_here
PHONE_NUMBER=+1234567890
```

### Optional Environment Variables

```env
# Server port (default: 8000)
PORT=8000

# Log level (default: INFO)
LOG_LEVEL=INFO

# Browser timeout in seconds (default: 30)
BROWSER_TIMEOUT=30
```

## Usage

### Starting the Server

Run the server with:

```bash
python src/main.py
```

Or using the module approach:

```bash
python -m src.main
```

### Testing the Server

Run the test suite to verify everything is working:

```bash
python tests/test_server.py
```

### Available Tools

The server provides the following MCP tools:

1. **shop_product**
   - Description: Automates the process of shopping for a product
   - Parameters:
     - `product_name` (string): Name of the product to search for
     - `max_price` (number, optional): Maximum price limit
     - `quantity` (number, optional): Quantity to purchase (default: 1)
   - Returns: Shopping result with status and details

### Example Usage with Claude Desktop

1. Install Claude Desktop from [Anthropic's website](https://claude.ai/download)
2. Configure Claude Desktop to use this MCP server by adding to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "shopping-agent": {
      "command": "python",
      "args": ["/path/to/shopping-agent-mcp/src/main.py"],
      "env": {
        "BROWSER_USE_API_KEY": "your_key",
        "BROWSER_USE_PROFILE_ID": "your_profile",
        "TARGET_EMAIL": "your_email",
        "TARGET_PASSWORD": "your_password",
        "PHONE_NUMBER": "your_phone"
      }
    }
  }
}
```

3. Restart Claude Desktop and you'll be able to use the shopping tools in your conversations.

## Development

### Project Structure

```
shopping-agent-mcp/
├── src/
│   ├── main.py              # Main server implementation
│   └── __init__.py
├── tests/
│   └── test_server.py       # Server tests
├── requirements.txt         # Python dependencies
├── .env.example            # Example environment variables
└── README.md              # This file
```

### Adding New Tools

To add a new tool to the MCP server:

1. Define a new function in `src/main.py` with appropriate parameters
2. Decorate it with `@mcp.tool()`
3. Update the documentation in this README
4. Add tests in `tests/test_server.py`

### Testing

Run the test suite:

```bash
python -m pytest tests/
```

For verbose output:

```bash
python -m pytest tests/ -v
```

## Troubleshooting

### Common Issues

1. **"Missing required environment variables" error**
   - Ensure all required variables are set in your `.env` file
   - Check that the `.env` file is in the project root directory
   - Verify variable names match exactly (case-sensitive)

2. **BrowserUse API errors**
   - Verify your API key is valid and has sufficient credits
   - Check that the profile ID exists and is accessible
   - Ensure network connectivity to BrowserUse API

3. **Import errors**
   - Make sure all dependencies are installed: `pip install -r requirements.txt`
   - Verify Python version is 3.8 or higher
   - Check that you're in the correct directory when running the server

4. **Server won't start**
   - Check port availability (default: 8000)
   - Verify no other MCP servers are running on the same port
   - Look for error messages in the console output

### Logging

The server provides different log levels:

- `DEBUG`: Detailed information for debugging
- `INFO`: General operational information (default)
- `WARNING`: Warning messages for potential issues
- `ERROR`: Error messages for failed operations

Set the `LOG_LEVEL` environment variable to control verbosity.

## Security Considerations

1. **Never commit `.env` files** to version control
2. **Use strong passwords** for your target accounts
3. **Regularly rotate API keys** when possible
4. **Monitor usage** of the BrowserUse API to prevent unexpected charges
5. **Keep dependencies updated** for security patches

## Support

For issues and questions:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review the error messages in console output
3. Ensure all prerequisites are met
4. Verify environment variables are correctly set

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]