# Troubleshooting Guide

This guide provides solutions to common issues you may encounter when installing, configuring, or using the ICAET MCP Server.

## Table of Contents
1. [Installation Issues](#installation-issues)
2. [Configuration Issues](#configuration-issues)
3. [Runtime Errors](#runtime-errors)
4. [API Connection Issues](#api-connection-issues)
5. [Cursor Integration Issues](#cursor-integration-issues)
6. [Logging and Debugging](#logging-and-debugging)
7. [Getting Help](#getting-help)

---

## Installation Issues

### Problem: `pip install` fails with dependency conflicts

**Error Message:**
```
ERROR: Cannot install icsaet-mcp because these package versions have conflicting dependencies.
```

**Solution:**
- Ensure you're using Python 3.12 or higher: `python --version`
- Create a fresh virtual environment:
  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  pip install git+https://github.com/[USERNAME]/icsaet-mcp.git
  ```
- Update pip before installing: `pip install --upgrade pip`

### Problem: `ModuleNotFoundError: No module named 'icsaet_mcp'`

**Solution:**
- Verify installation: `pip list | grep icsaet`
- Reinstall the package: `pip install --force-reinstall git+https://github.com/[USERNAME]/icsaet-mcp.git`
- Check you're in the correct virtual environment

### Problem: Permission denied during installation

**Solution:**
- Use a virtual environment (recommended) instead of system Python
- On Linux/Mac: Use `sudo` only if absolutely necessary
- On Windows: Run terminal as Administrator

---

## Configuration Issues

### Problem: "Missing required credentials" error

**Error Message:**
```
ValueError: Missing required credentials. Set ICAET_API_KEY and USER_EMAIL environment variables.
```

**Solution:**
Add environment variables to your Cursor MCP configuration file (`~/.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "icsaet": {
      "command": "python",
      "args": ["-m", "icsaet_mcp"],
      "env": {
        "ICAET_API_KEY": "your-actual-api-key-here",
        "USER_EMAIL": "your-email@example.com"
      }
    }
  }
}
```

**Important:** Replace `your-actual-api-key-here` and `your-email@example.com` with your real credentials.

### Problem: Invalid API key format

**Error Message:**
```
Error: Authentication failed. Please check your ICAET_API_KEY.
```

**Solution:**
- Verify your API key is correct (no extra spaces, quotes, or newlines)
- Check that the API key hasn't expired
- Ensure the key has the necessary permissions
- Contact ICAET support to regenerate your API key if needed

### Problem: Environment variables not being read

**Solution:**
- Restart Cursor IDE completely after updating `mcp.json`
- Verify the configuration file path is correct: `~/.cursor/mcp.json`
- Check JSON syntax is valid (use a JSON validator)
- Ensure no typos in environment variable names (case-sensitive)

---

## Runtime Errors

### Problem: Server crashes immediately on startup

**Solution:**
1. Check the Cursor MCP server logs (see [Logging and Debugging](#logging-and-debugging))
2. Verify all dependencies are installed: `pip check`
3. Test server manually:
   ```bash
   ICAET_API_KEY=your-key USER_EMAIL=your-email python -m icsaet_mcp
   ```
4. Look for import errors or missing modules

### Problem: "Request timeout" errors

**Error Message:**
```
Error querying ICAET API: Request timeout after 30 seconds
```

**Solution:**
- Check your internet connection
- The ICAET API may be experiencing high load; try again later
- Complex queries may take longer; this is expected
- If persistent, check if the API endpoint is accessible: `curl https://icaet-api-url`

### Problem: Unexpected JSON parsing errors

**Error Message:**
```
Error: Failed to parse API response
```

**Solution:**
- Enable DEBUG logging to see the raw response (see [Logging and Debugging](#logging-and-debugging))
- This may indicate an API change; check for updates to the MCP server
- Report the issue with DEBUG logs to support

---

## API Connection Issues

### Problem: Cannot connect to ICAET API

**Error Message:**
```
Error querying ICAET API: Connection refused
Error querying ICAET API: Network unreachable
```

**Solution:**
- Verify internet connectivity: `ping 8.8.8.8`
- Check if you're behind a corporate firewall or proxy
- If using a proxy, configure it:
  ```bash
  export HTTP_PROXY=http://proxy.example.com:8080
  export HTTPS_PROXY=http://proxy.example.com:8080
  ```
- Verify the ICAET API endpoint is accessible
- Check if your network blocks certain ports

### Problem: 401 Unauthorized or 403 Forbidden errors

**Error Message:**
```
Error: API request failed with status 401: Unauthorized
Error: API request failed with status 403: Forbidden
```

**Solution:**
- Verify `ICAET_API_KEY` is correct
- Verify `USER_EMAIL` is correct
- Check if your API key has been revoked or expired
- Ensure your account has necessary permissions
- Contact ICAET support to verify account status

### Problem: 429 Too Many Requests errors

**Error Message:**
```
Error: API request failed with status 429: Too Many Requests
```

**Solution:**
- You've hit the API rate limit
- Wait a few minutes before trying again
- Consider spacing out your queries
- Contact ICAET support to request higher rate limits if needed

---

## Cursor Integration Issues

### Problem: Cursor doesn't detect the MCP server

**Solution:**
1. Verify `mcp.json` is in the correct location: `~/.cursor/mcp.json`
2. Check JSON syntax is valid (no trailing commas, proper quotes)
3. Restart Cursor IDE completely
4. Check Cursor MCP server panel for error messages
5. Verify Python is in your PATH: `which python` (Linux/Mac) or `where python` (Windows)

### Problem: MCP server appears but doesn't respond

**Solution:**
1. Check Cursor's MCP server logs for errors
2. Verify environment variables are set in `mcp.json`
3. Test the server manually outside Cursor:
   ```bash
   ICAET_API_KEY=your-key USER_EMAIL=your-email python -m icsaet_mcp
   ```
4. Look for authentication or network errors in logs

### Problem: Server listed as "disconnected" or "failed"

**Solution:**
- Check the error message in Cursor's MCP server panel
- Verify Python version: `python --version` (must be 3.12+)
- Check that `icsaet-mcp` package is installed in the Python environment Cursor is using
- Ensure the `command` in `mcp.json` points to the correct Python executable
- Try using absolute path: `"command": "/path/to/python"`

---

## Logging and Debugging

### Log File Locations

The ICAET MCP server writes logs to stderr, which Cursor captures. To view logs:

1. **In Cursor IDE:**
   - Open the MCP server panel
   - Click on "icsaet" server
   - View logs in the output panel

2. **Manual testing (terminal):**
   - Logs appear directly in the terminal where you run the server

### Enable Debug Logging

Set the `ICAET_LOG_LEVEL` environment variable to `DEBUG` for detailed logging:

**In Cursor's `mcp.json`:**
```json
{
  "mcpServers": {
    "icsaet": {
      "command": "python",
      "args": ["-m", "icsaet_mcp"],
      "env": {
        "ICAET_API_KEY": "your-key",
        "USER_EMAIL": "your-email@example.com",
        "ICAET_LOG_LEVEL": "DEBUG"
      }
    }
  }
}
```

**Manual testing:**
```bash
ICAET_LOG_LEVEL=DEBUG ICAET_API_KEY=your-key USER_EMAIL=your-email python -m icsaet_mcp
```

### What Debug Logs Show

Debug logging includes:
- Server initialization details
- Full API request URLs and headers (credentials redacted)
- Complete API responses
- Detailed error stack traces
- Environment variable validation

### Testing Without Cursor

To verify the server works independently of Cursor:

```bash
# Set credentials
export ICAET_API_KEY=your-actual-key
export USER_EMAIL=your-email@example.com
export ICAET_LOG_LEVEL=DEBUG

# Run the server
python -m icsaet_mcp
```

If the server starts without errors, the issue is likely with Cursor integration, not the server itself.

---

## Getting Help

### Before Requesting Support

Please gather the following information:
1. Python version: `python --version`
2. Package version: `pip show icsaet-mcp`
3. Operating system and version
4. Complete error message (copy-paste, don't screenshot)
5. Debug logs (set `ICAET_LOG_LEVEL=DEBUG`)
6. Your `mcp.json` configuration (remove sensitive credentials)

### Support Escalation Path

1. **Check this troubleshooting guide** for common issues
2. **Review the [README.md](README.md)** for configuration examples
3. **Search existing GitHub issues** for similar problems
4. **Create a new GitHub issue** with:
   - Clear description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment information (from above)
   - Debug logs (credentials redacted)

### Contact Information

- **GitHub Issues:** https://github.com/[USERNAME]/icsaet-mcp/issues
- **Documentation:** See [README.md](README.md)

### Security Issues

If you've discovered a security vulnerability, **do not** open a public GitHub issue. Instead:
- Email security concerns directly to the maintainers
- Provide detailed information privately
- Allow time for a fix before public disclosure

---

## Quick Reference: Common Commands

```bash
# Install from GitHub
pip install git+https://github.com/[USERNAME]/icsaet-mcp.git

# Verify installation
python -c "import icsaet_mcp; print('Installed successfully')"

# Test server (replace with your credentials)
ICAET_API_KEY=your-key USER_EMAIL=your-email python -m icsaet_mcp

# Enable debug logging
ICAET_LOG_LEVEL=DEBUG ICAET_API_KEY=your-key USER_EMAIL=your-email python -m icsaet_mcp

# Check Python version
python --version

# List installed packages
pip list | grep icsaet
```

---

**Still having issues?** Open a GitHub issue with detailed information, and we'll help you resolve it.

