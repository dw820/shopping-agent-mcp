# Shopping Agent MCP Server

A Model Context Protocol (MCP) server that provides shopping automation capabilities through AI agents.

## Overview

This MCP server enables AI assistants to perform shopping tasks on e-commerce websites. It provides tools for product search, price comparison, and automated purchasing workflows.

## Features

- **Product Search**: Find products across multiple retailers
- **Price Comparison**: Compare prices for the same product
- **Automated Purchasing**: Complete checkout processes automatically
- **Browser Automation**: Headless browser operations for web interactions
- **Secure Authentication**: Safe handling of credentials and payment information

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Required environment variables (see Configuration section)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/shopping-agent-mcp.git
cd shopping-agent-mcp

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your values
```

### Running the Server

```bash
# Start the MCP server
python -m src.main
```

## Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Browser automation API credentials
BROWSER_USE_API_KEY=your_browser_use_api_key
BROWSER_USE_PROFILE_ID=your_profile_id

# Target website credentials
TARGET_EMAIL=your_email@example.com
TARGET_PASSWORD=your_password
PHONE_NUMBER=your_phone_number

# Optional: Server configuration
SERVER_HOST=localhost
SERVER_PORT=8000
LOG_LEVEL=INFO
```

### Required Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `BROWSER_USE_API_KEY` | API key for Browser.use service | Yes |
| `BROWSER_USE_PROFILE_ID` | Profile ID for browser sessions | Yes |
| `TARGET_EMAIL` | Email for target website login | Yes |
| `TARGET_PASSWORD` | Password for target website login | Yes |
| `PHONE_NUMBER` | Phone number for verification | Yes |

## API Documentation

### Available Tools

#### `shop_product`

Search for and purchase products on supported e-commerce websites.

**Parameters:**
- `product_name` (string, required): Name of the product to search for
- `max_price` (number, optional): Maximum price limit in USD
- `retailer` (string, optional): Specific retailer to search (default: "amazon")
- `quantity` (integer, optional): Number of items to purchase (default: 1)

**Returns:**
- JSON object containing purchase confirmation details including:
  - `success`: Boolean indicating if purchase was successful
  - `order_id`: Unique identifier for the order
  - `product_name`: Name of purchased product
  - `price`: Final purchase price
  - `estimated_delivery`: Estimated delivery date

**Example Usage:**
```python
# Through MCP client
result = await client.call_tool("shop_product", {
    "product_name": "wireless headphones",
    "max_price": 150,
    "retailer": "bestbuy",
    "quantity": 1
})
```

### Server Endpoints

The server runs on `http://localhost:8000` by default and provides:

- **HTTP Transport**: MCP-over-HTTP endpoint at `/`
- **Health Check**: `GET /health` returns server status
- **Tool List**: `GET /tools` returns available tools

## Development

### Project Structure

```
shopping-agent-mcp/
├── src/
│   ├── main.py              # Main server entry point
│   ├── tools/
│   │   └── shopping.py      # Shopping tool implementations
│   └── utils/
│       └── browser.py       # Browser automation utilities
├── tests/
│   └── test_server.py       # Server tests
├── requirements.txt         # Python dependencies
├── .env.example            # Environment template
└── README.md              # This file
```

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_server.py -v
```

### Adding New Tools

1. Create a new function in `src/tools/` directory
2. Decorate with `@mcp.tool()` decorator
3. Import and register in `src/main.py`
4. Add tests in `tests/`

Example:
```python
# src/tools/price_tracker.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("price-tracker")

@mcp.tool()
async def track_price(product_url: str, target_price: float) -> dict:
    """Track product price and notify when it drops below target."""
    # Implementation here
    return {"tracking": True, "product_url": product_url}
```

## Troubleshooting

### Common Issues

1. **Missing Environment Variables**
   ```
   ValueError: Missing required environment variables: BROWSER_USE_API_KEY
   ```
   Solution: Ensure all required variables are set in `.env` file.

2. **Browser Automation Failures**
   - Check Browser.use API key validity
   - Verify profile ID exists in your Browser.use account
   - Ensure network connectivity to Browser.use service

3. **Authentication Failures**
   - Verify target website credentials are correct
   - Check if website requires additional verification (2FA, captcha)
   - Ensure phone number format is correct

### Logging

Set `LOG_LEVEL` environment variable to control verbosity:
- `DEBUG`: Detailed debugging information
- `INFO`: General operational information (default)
- `WARNING`: Only warnings and errors
- `ERROR`: Only errors

## Security Considerations

- Never commit `.env` file to version control
- Use environment variables for sensitive data
- Regularly rotate API keys and credentials
- Monitor server access logs for unauthorized usage

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add or update tests
5. Submit a pull request

Please ensure all tests pass and documentation is updated.

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:
- Open a GitHub issue
- Check existing issues for solutions
- Refer to the MCP documentation at https://modelcontextprotocol.io