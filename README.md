# Shopping Agent MCP Server

> **Automated Target.com shopping agent** — Search products, add to cart, and fill checkout with a single function call.

## Overview

This shopping agent uses [Browser Use SDK](https://browser-use.com) to automate the Target.com shopping experience. It maintains persistent login state via browser profiles and can:

- 🔐 **Login** to Target.com with stored credentials
- 🔍 **Search** for specific products by name
- 💰 **Find the cheapest** relevant product from search results
- 🛒 **Add to cart** and proceed to checkout
- 📦 **Fill shipping address** with provided information
- 📸 **Stop before purchase** with screenshot of final order review

### Core Function: `run_target_shopping_task()`

```python
async def run_target_shopping_task(
    product_name: str,      # Product to search for (e.g., "protein bars")
    first_name: str,        # Shipping first name
    last_name: str,         # Shipping last name
    address: str,           # Street address
    unit: str,              # Apartment/unit number
    city: str,              # City name
    state: str,             # State abbreviation (e.g., "CA")
    zip_code: str,          # ZIP code
)
```

The function will:
1. Login to Target.com (skipping all popups)
2. Search for `product_name` and find the cheapest relevant item
3. Add the item to cart
4. Proceed to checkout with "Shipping" method
5. Fill in the shipping address with provided details
6. Stop at the final order review page (does NOT place order)
7. Report the item name and total amount

## Environment Variables

Create a `.env` file with:

```bash
BROWSER_USE_API_KEY=bu_your_api_key_here
BROWSER_USE_PROFILE_ID=your_profile_id_here
TARGET_EMAIL=your_target_email
TARGET_PASSWORD=your_target_password
PHONE_NUMBER=your_phone_number
```
## Quick Start (Local Development)

```bash
# Install uv package manager
brew install uv  # or pip install uv

# Install dependencies
uv sync --no-dev

# Test
uv run python tests/test_server.py

# Run
uv run main
```

## Project Structure

```
.
├── pyproject.toml      # Package configuration with dependencies
├── main.py             # Entry point (Dedalus expects this)
├── src/
│   ├── __init__.py
│   └── main.py         # Main MCP server code
├── config/
│   └── .env.example    # Environment template
└── tests/
    └── test_server.py  # Server tests
```

## Deploy to Dedalus

```bash
dedalus deploy . --name "shopping-agent"
```

## License

MIT