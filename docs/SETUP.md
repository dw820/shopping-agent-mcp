# Setup Guide

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Verification](#verification)
5. [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements

- **Operating System**: Windows 10+, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **Python**: Version 3.8 or higher
- **Memory**: Minimum 4GB RAM (8GB recommended for browser automation)
- **Disk Space**: 500MB free space

### Software Requirements

1. **Python 3.8+**
   - Verify installation: `python --version` or `python3 --version`
   - Download from [python.org](https://www.python.org/downloads/)

2. **pip** (Python package manager)
   - Usually installed with Python
   - Verify: `pip --version`

3. **Git** (optional, for cloning repository)
   - Verify: `git --version`

### Service Accounts

1. **BrowserUse Account**
   - Sign up at [BrowserUse](https://browseruse.com)
   - Obtain API key from dashboard
   - Create or obtain profile ID

2. **Target Website Account**
   - Create account on target shopping website
   - Ensure account is active and can make purchases
   - Note login credentials (email/password)

## Installation

### Step 1: Clone Repository

```bash
# Clone the repository
git clone <repository-url>
cd shopping-agent-mcp

# Or download and extract ZIP file
# Navigate to extracted directory
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
# Install from requirements.txt
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
# Check installed packages
pip list | grep -E "mcp|browser-use"

# Expected output should show:
# mcp
# browser-use
# python-dotenv
```

## Configuration

### Step 1: Create Environment File

Create a `.env` file in the project root directory:

```bash
# Create .env file
touch .env  # On macOS/Linux
# or create manually in text editor
```

### Step 2: Configure Environment Variables

Edit the `.env` file with your credentials:

```env
# BrowserUse Configuration
# Get these from your BrowserUse dashboard
BROWSER_USE_API_KEY=bu_1234567890abcdef
BROWSER_USE_PROFILE_ID=profile_12345

# Target Website Credentials
# Use a dedicated account for automation
TARGET_EMAIL=automation@example.com
TARGET_PASSWORD=SecurePassword123!
PHONE_NUMBER=+1234567890
```

### Step 3: Security Considerations

1. **Never commit `.env` to version control**
   - Add `.env` to `.gitignore`
   - Use `.env.example` for template

2. **Use different accounts for development/production**
   - Development: Test accounts with limited permissions
   - Production: Dedicated automation accounts

3. **Rotate credentials regularly**
   - Change passwords every 90 days
   - Update API keys as needed

## Verification

### Step 1: Test Environment Variables

Create a test script to verify configuration:

```python
# test_env.py
import os
from dotenv import load_dotenv

load_dotenv()

required_vars = [
    "BROWSER_USE_API_KEY",
    "BROWSER_USE_PROFILE_ID", 
    "TARGET_EMAIL",
    "TARGET_PASSWORD",
    "PHONE_NUMBER"
]

print("Checking environment variables...")
for var in required_vars:
    value = os.getenv(var)
    if value:
        print(f"✓ {var}: {value[:10]}...")  # Show first 10 chars only
    else:
        print(f"✗ {var}: MISSING")

print("\nAll variables present!" if all(os.getenv(v) for v in required_vars) 
      else "\nSome variables missing!")
```

Run the test:
```bash
python test_env.py
```

### Step 2: Run Server Tests

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

### Step 3: Start the Server

```bash
python src/main.py
```

Expected output:
```
🛒 Starting Shopping Agent MCP Server...
🔧 Available tools: shop_product
```

## Troubleshooting

### Common Issues

#### Issue 1: Python/Pip Not Found
**Symptoms**: `python: command not found` or `pip: command not found`

**Solutions**:
- Ensure Python is installed: `python --version`
- Use `python3` and `pip3` on some systems
- Add Python to PATH environment variable

#### Issue 2: Import Errors
**Symptoms**: `ModuleNotFoundError` when running tests or server

**Solutions**:
- Verify virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`
- Check Python version compatibility

#### Issue 3: Missing Environment Variables
**Symptoms**: `ValueError: Missing required environment variables`

**Solutions**:
- Verify `.env` file exists in project root
- Check variable names match exactly
- Ensure no trailing spaces in `.env` file
- Restart terminal after creating `.env` file

#### Issue 4: BrowserUse Authentication Failed
**Symptoms**: Browser automation fails with authentication errors

**Solutions**:
- Verify API key is valid and not expired
- Check profile ID exists in BrowserUse dashboard
- Ensure account has sufficient credits/quotas

### Debug Mode

Enable debug logging for more information:

```python
# Add to src/main.py before mcp.run()
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Getting Help

1. **Check Logs**: Look for error messages in console output
2. **Verify Steps**: Go through setup guide step by step
3. **Test Components**: Test each component independently
4. **Community Support**: [Add community forum or support channel]

## Next Steps

After successful setup:

1. **Test the tool**: Use an MCP client to call `shop_product`
2. **Monitor performance**: Check execution times and success rates
3. **Scale up**: Consider running multiple instances for production
4. **Add monitoring**: Implement logging and alerting

## Maintenance

### Regular Tasks

1. **Update dependencies**: `pip install -r requirements.txt --upgrade`
2. **Rotate credentials**: Update `.env` file with new credentials
3. **Check quotas**: Monitor BrowserUse API usage and quotas
4. **Review logs**: Check for errors or performance issues

### Backup Configuration

Keep backup of `.env` file in secure location:

```bash
# Backup .env file
cp .env .env.backup

# Restore from backup
cp .env.backup .env
```

## Support

For additional help:
- Review API documentation in `docs/API.md`
- Check example configurations
- Contact [support email or channel]