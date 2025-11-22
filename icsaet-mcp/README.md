# ICAET MCP Server

A Model Context Protocol (MCP) server that provides Cursor IDE with direct access to the ICAET (International Conference on Advanced Engineering Theory) knowledge base API.

## Features

- **MCP Protocol Implementation:** Full integration with Cursor IDE using the fastmcp framework
- **ICAET Knowledge Base Access:** Query the ICAET API directly from your coding environment
- **Structured Logging:** Configurable log levels (DEBUG, INFO, WARNING, ERROR) for troubleshooting
- **Robust Error Handling:** Comprehensive error handling for API failures, network issues, and timeouts
- **Environment-Based Configuration:** Secure credential management via environment variables
- **Comprehensive Test Suite:** Full unit and integration tests with >80% code coverage
- **Type Safety:** Fully typed Python codebase for reliability and maintainability

## Installation

### From GitHub

```bash
pip install git+https://github.com/[USERNAME]/icsaet-mcp.git
```

Replace `[USERNAME]` with the actual GitHub username or organization.

### Development Installation

For development or contributions:

```bash
# Clone the repository
git clone https://github.com/[USERNAME]/icsaet-mcp.git
cd icsaet-mcp

# Install in editable mode with development dependencies
pip install -e ".[dev]"
```

## Configuration

### Cursor MCP Settings

Configure the MCP server in Cursor by editing your MCP configuration file:

**File Location:** `~/.cursor/mcp.json` (or `~/.cursor/config.json`)

**Configuration:**

```json
{
  "mcpServers": {
    "icsaet": {
      "command": "python",
      "args": ["-m", "icsaet_mcp"],
      "env": {
        "ICAET_API_KEY": "your-api-key-here",
        "USER_EMAIL": "your-email@example.com",
        "ICAET_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

**Important:** Replace the placeholder values with your actual credentials.

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ICAET_API_KEY` | Yes | None | Your ICAET API authentication key |
| `USER_EMAIL` | Yes | None | Your registered email address |
| `ICAET_LOG_LEVEL` | No | `INFO` | Logging level: `DEBUG`, `INFO`, `WARNING`, `ERROR` |

**Notes:**
- `ICAET_API_KEY` and `USER_EMAIL` are required for authentication
- Use `ICAET_LOG_LEVEL=DEBUG` for detailed troubleshooting
- Credentials are never logged (automatically redacted in DEBUG mode)

## Usage

Once configured, the ICAET MCP server runs automatically when you open Cursor IDE. You can query the ICAET knowledge base directly through Cursor's AI assistant.

### Example Queries

Ask questions like:

1. **Research Paper Search:**
   ```
   "What are the latest papers on machine learning optimization in ICAET?"
   ```

2. **Author Information:**
   ```
   "Find papers by Dr. Smith published at ICAET conferences"
   ```

3. **Topic Exploration:**
   ```
   "What research has been done on quantum computing at ICAET?"
   ```

4. **Conference Details:**
   ```
   "Show me information about ICAET 2024 conference proceedings"
   ```

5. **Citation Research:**
   ```
   "Find highly cited papers on neural networks from ICAET"
   ```

### Expected Response Format

The server returns structured data from the ICAET API, which Cursor's AI assistant will format into readable responses. Responses typically include:
- Paper titles and abstracts
- Author information
- Publication dates
- Conference details
- Citations and references

## Troubleshooting

### Quick Solutions

**Problem: "Missing required credentials" error**
- **Solution:** Add `ICAET_API_KEY` and `USER_EMAIL` to your `mcp.json` configuration file

**Problem: Server not appearing in Cursor**
- **Solution:** Verify `mcp.json` file location and syntax, then restart Cursor IDE

**Problem: Connection errors**
- **Solution:** Check your internet connection and verify API credentials are correct

**Problem: Timeout errors**
- **Solution:** Complex queries may take time; this is normal. Check your network connection if persistent.

### Detailed Troubleshooting

For comprehensive troubleshooting guidance, see the [TROUBLESHOOTING.md](TROUBLESHOOTING.md) guide, which covers:
- Installation issues
- Configuration problems
- Runtime errors
- API connection issues
- Cursor integration issues
- Logging and debugging techniques
- Support escalation

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/[USERNAME]/icsaet-mcp.git
cd icsaet-mcp

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests with coverage
pytest

# Run specific test file
pytest tests/test_tools.py

# Run with verbose output
pytest -v

# Generate HTML coverage report
pytest --cov-report=html
# Open htmlcov/index.html in your browser
```

### Code Quality

```bash
# Format code with Black
black src/ tests/

# Lint with Ruff
ruff check src/ tests/

# Type checking (if using mypy)
mypy src/
```

### Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes with tests
4. Ensure all tests pass: `pytest`
5. Ensure code coverage remains >80%
6. Format code: `black src/ tests/`
7. Commit with conventional commit messages
8. Push and create a pull request

**Code Standards:**
- Follow PEP 8 style guidelines
- Add type hints to all functions
- Write tests for new features
- Maintain >80% test coverage
- Document public APIs

## Requirements

- **Python:** 3.12 or higher
- **Dependencies:**
  - fastmcp >= 0.1.0
  - httpx >= 0.24.0
- **Development Dependencies:**
  - pytest >= 7.4.0
  - pytest-asyncio >= 0.21.0
  - pytest-httpx >= 0.22.0
  - pytest-cov >= 4.1.0
  - black >= 23.0.0
  - ruff >= 0.1.0

## Project Structure

```
icsaet-mcp/
├── src/
│   └── icsaet_mcp/
│       ├── __init__.py
│       ├── __main__.py          # Entry point
│       ├── server.py            # MCP server implementation
│       ├── tools.py             # MCP tools (query function)
│       ├── prompts.py           # MCP prompts and resources
│       ├── utils.py             # Utility functions
│       └── logging_config.py    # Logging configuration
├── tests/
│   ├── test_server.py           # Server tests
│   ├── test_tools.py            # Tools tests
│   ├── test_prompts.py          # Prompts tests
│   ├── test_utils.py            # Utils tests
│   ├── test_logging.py          # Logging tests
│   ├── test_integration.py      # Integration tests
│   ├── mock_server.py           # Mock API server
│   └── conftest.py              # Pytest configuration
├── pyproject.toml               # Project configuration
├── README.md                    # This file
├── CHANGELOG.md                 # Version history
├── TROUBLESHOOTING.md           # Detailed troubleshooting
└── LICENSE                      # MIT License
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

### Getting Help

1. **Documentation:** Read this README and [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. **GitHub Issues:** Search [existing issues](https://github.com/[USERNAME]/icsaet-mcp/issues)
3. **New Issue:** Create a [new issue](https://github.com/[USERNAME]/icsaet-mcp/issues/new) with:
   - Clear problem description
   - Steps to reproduce
   - Environment information (Python version, OS)
   - Error messages and logs

### Reporting Issues

When reporting issues, please include:
- Python version: `python --version`
- Package version: `pip show icsaet-mcp`
- Operating system and version
- Complete error message
- Debug logs (set `ICAET_LOG_LEVEL=DEBUG`)
- Configuration file (remove credentials)

### Security Vulnerabilities

If you discover a security vulnerability, please **do not** open a public issue. Email security concerns directly to the maintainers.

---

**Built with [fastmcp](https://github.com/jlowin/fastmcp)** | **Powered by the ICAET Knowledge Base**
