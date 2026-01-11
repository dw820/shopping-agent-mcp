# Shopping Agent MCP Server

A Model Context Protocol (MCP) server that provides shopping automation capabilities through AI agents.

## Features

- **Product Shopping Tool**: Automate product searches and purchases
- **Browser Automation**: Uses BrowserUse API for web automation
- **Environment Configuration**: Secure configuration via environment variables
- **FastMCP Integration**: Built on the FastMCP framework for MCP servers

## Quick Start

### Prerequisites

- Python 3.8 or higher
- BrowserUse API key and profile ID
- Target website credentials

### Installation

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

### Running the Server

```bash
python src/main.py
```

## Configuration

### Required Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# BrowserUse API Configuration
BROWSER_USE_API_KEY=your_browseruse_api_key
BROWSER_USE_PROFILE_ID=your_browseruse_profile_id

# Target Website Credentials
TARGET_EMAIL=your_email@example.com
TARGET_PASSWORD=your_password
PHONE_NUMBER=your_phone_number
```

### Optional Environment Variables

```env
# Server Configuration
PORT=8000  # Default: 8000
HOST=0.0.0.0  # Default: 0.0.0.0
LOG_LEVEL=INFO  # Default: INFO

# Browser Configuration
BROWSER_TIMEOUT=30  # Default: 30 seconds
HEADLESS=false  # Default: false
```

## API Documentation

### Available Tools

#### `shop_product`

Searches for and purchases a product on supported e-commerce websites.

**Parameters:**
- `product_name` (string, required): Name of the product to search for
- `max_price` (number, optional): Maximum price limit for the product
- `quantity` (integer, optional): Quantity to purchase (default: 1)
- `website` (string, optional): Target website (default: "amazon")

**Returns:**
- JSON object containing purchase status, order details, and product information

**Example Usage:**
```python
# Through MCP client
result = await client.call_tool("shop_product", {
    "product_name": "wireless headphones",
    "max_price": 100,
    "quantity": 2,
    "website": "amazon"
})
```

### Server Endpoints

The server exposes the following endpoints when running in HTTP mode:

- `POST /tools/call` - Call a tool by name
- `GET /tools/list` - List all available tools
- `GET /health` - Health check endpoint
- `POST /prompts/list` - List available prompts
- `POST /prompts/get` - Get a specific prompt

## Development

### Project Structure

```
shopping-agent-mcp/
├── src/
│   ├── main.py              # Main server implementation
│   └── tools/
│       └── shopping.py      # Shopping tool implementation
├── tests/
│   └── test_server.py       # Server tests
├── requirements.txt         # Python dependencies
├── pyproject.toml          # Project configuration
└── README.md               # This file
```

### Running Tests

```bash
python -m pytest tests/
```

Or run the comprehensive test suite:

```bash
python tests/test_server.py
```

### Adding New Tools

1. Create a new tool function in `src/tools/` directory
2. Decorate it with `@mcp.tool()`
3. Import and register it in `src/main.py`
4. Update documentation

Example tool implementation:
```python
@mcp.tool()
async def my_new_tool(param1: str, param2: int) -> dict:
    """Description of what the tool does."""
    # Tool implementation
    return {"result": "success"}
```

## Deployment

### Docker

Build and run with Docker:

```bash
docker build -t shopping-agent-mcp .
docker run -p 8000:8000 --env-file .env shopping-agent-mcp
```

### Cloud Deployment

The server can be deployed to any cloud platform that supports Python applications:

- **AWS**: Deploy to ECS or Lambda
- **Google Cloud**: Deploy to Cloud Run or App Engine
- **Azure**: Deploy to Container Instances or App Service

## Troubleshooting

### Common Issues

1. **Missing Environment Variables**
   - Error: `ValueError: Missing required environment variables`
   - Solution: Ensure all required variables are set in `.env` file

2. **BrowserUse API Errors**
   - Error: BrowserUse API connection failures
   - Solution: Verify API key and profile ID are correct

3. **Authentication Failures**
   - Error: Target website login failures
   - Solution: Check credentials and website availability

### Logging

Set `LOG_LEVEL` environment variable to control verbosity:
- `DEBUG`: Detailed debugging information
- `INFO`: General operational information (default)
- `WARNING`: Warning messages only
- `ERROR`: Error messages only

## Security Considerations

1. **Credentials**: Never commit `.env` files or hardcode credentials
2. **API Keys**: Rotate API keys regularly
3. **Input Validation**: All tool inputs are validated server-side
4. **Rate Limiting**: Implement rate limiting for production deployments

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add or update tests
5. Update documentation
6. Submit a pull request

## License

[Add license information here]

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review existing GitHub issues
3. Create a new issue with detailed information