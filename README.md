# Shopping Agent MCP Server

An MCP server for shopping agent functionality.

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