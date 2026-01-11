# Shopping Agent MCP Server

A Model Context Protocol (MCP) server that provides shopping automation capabilities through browser automation tools.

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

### Configuration

Create a `.env` file in the project root with the following variables:

```env
# BrowserUse API Configuration
BROWSER_USE_API_KEY=your_browseruse_api_key
BROWSER_USE_PROFILE_ID=your_profile_id

# Target Website Credentials
TARGET_EMAIL=your_email@example.com
TARGET_PASSWORD=your_password
PHONE_NUMBER=your_phone_number
```

### Running the Server

Start the MCP server:

```bash
python src/main.py
```

The server will start and display available tools.

## Available Tools

### shop_product

Automates the process of searching for and purchasing a product.

**Parameters:**
- `product_name` (string): The name of the product to search for
- `max_price` (optional, number): Maximum price limit for the product
- `quantity` (optional, number): Quantity to purchase (default: 1)

**Returns:**
- JSON object with purchase status and details

**Example Usage:**
```python
# Through MCP client
result = await client.call_tool("shop_product", {
    "product_name": "wireless headphones",
    "max_price": 150,
    "quantity": 2
})
```

## Development

### Project Structure

```
shopping-agent-mcp/
├── src/
│   └── main.py          # Main server implementation
├── tests/
│   └── test_server.py   # Server tests
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

### Testing

Run the test suite:

```bash
python tests/test_server.py
```

### Dependencies

Key dependencies:
- `mcp`: Model Context Protocol framework
- `browser-use`: Browser automation library
- `python-dotenv`: Environment variable management

See `requirements.txt` for complete list.

## API Reference

### Main Server (`src/main.py`)

#### `main() -> None`
Starts the MCP server with streamable HTTP transport.

#### `get_env_vars() -> dict`
Retrieves and validates required environment variables.

**Returns:** Dictionary of environment variables

**Raises:** `ValueError` if any required variable is missing

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `BROWSER_USE_API_KEY` | API key for BrowserUse service | Yes |
| `BROWSER_USE_PROFILE_ID` | Profile ID for browser automation | Yes |
| `TARGET_EMAIL` | Email for target website login | Yes |
| `TARGET_PASSWORD` | Password for target website login | Yes |
| `PHONE_NUMBER` | Phone number for verification | Yes |

## Troubleshooting

### Common Issues

1. **Missing environment variables**
   - Ensure all required variables are set in `.env` file
   - Check variable names for typos

2. **Import errors**
   - Verify all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version compatibility

3. **Browser automation failures**
   - Verify BrowserUse API key and profile ID are valid
   - Check target website accessibility

### Getting Help

- Check the test output: `python tests/test_server.py`
- Review environment variable configuration
- Ensure network connectivity to BrowserUse API

## License

[Add license information here]

## Contributing

[Add contribution guidelines here]