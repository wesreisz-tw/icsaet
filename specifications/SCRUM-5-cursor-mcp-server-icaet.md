# SCRUM-5: Cursor MCP Server for ICAET Query Access

## Issue Details

- **Issue Key:** SCRUM-5
- **Status:** To Do
- **Priority:** Medium
- **Created:** 2025-11-22T14:53:41.684-0500
- **Updated:** 2025-11-22T14:58:05.803-0500
- **Reporter:** Wesley Reisz (wes@wesleyreisz.com)
- **Assignee:** Unassigned
- **Story Points:** Not set
- **Labels:** None
- **Components:** None

## Summary

Cursor MCP Server for ICAET Query Access

## User Story

### As a

Developer using Cursor IDE who wants to query the ICAET knowledge base.

### I want to

Configure a local MCP server in Cursor that allows me to ask questions against the ICAET API using simple environment variable configuration.

### So that

I can ask multi-turn questions against the ICAET Query API directly from Cursor without managing complex authentication flows, while keeping the existing ICAET API completely untouched.

---

# High-Level Description of the System

A local MCP server runs on the developer's machine and integrates with Cursor IDE. The developer configures their ICAET API key and email as environment variables in Cursor's MCP configuration. The MCP server exposes a query tool and helpful prompts that enable natural language interaction with the ICAET knowledge base.

The MCP server:

1. Receives queries from Cursor
2. Calls the existing ICAET API with the configured API key and email
3. Returns results to Cursor
4. Provides helpful prompts and examples to guide users

---

# Architecture Components

## Local Resources

* **Python MCP Server** (using fastmcp framework) - Runs locally on developer's machine
* **Environment Variables** - Stores ICAET_API_KEY and USER_EMAIL

## External Services

* **Cursor IDE** - MCP client interface
* **Existing ICAET API** - [https://icaet-dev.wesleyreisz.com/query](https://icaet-dev.wesleyreisz.com/query) (UNTOUCHED)

## No AWS Infrastructure Required

* MCP server runs entirely locally
* No Lambda, API Gateway, or other cloud resources needed

---

# Request Flow

```
1. Developer configures MCP server in Cursor
   ↓
2. Developer opens Cursor IDE
   ↓
3. Cursor starts local MCP server process
   ↓
4. Developer asks: "What did Leslie Miley talk about?"
   ↓
5. Cursor sends query to MCP server
   ↓
6. MCP server:
   - Receives question from Cursor
   - Reads ICAET_API_KEY and USER_EMAIL from environment
   - Calls ICAET API: POST https://icaet-dev.wesleyreisz.com/query
     Headers: x-api-key: {ICAET_API_KEY}
     Body: {"email": "{USER_EMAIL}", "question": "What did Leslie Miley talk about?"}
   - Returns ICAET response
   ↓
7. Cursor displays results to developer
```

---

# Acceptance Criteria

## 1. MCP Server Implementation

* Python-based MCP server using fastmcp framework
* Single `query` tool that accepts a question parameter
* Tool calls ICAET API with configured credentials
* Handles errors gracefully (API errors, network issues, missing credentials)
* Logs appropriately (no sensitive data in logs)

## 2. MCP Server Prompts

* Prompt that explains what ICAET is and how to use it
    * \[STUB: To be filled in with ICAET description\]
* Prompt that provides example questions
    * \[STUB: To be filled in with example queries\]
* Prompt that helps users format their questions better
    * \[STUB: To be filled in with formatting guidance\]

## 3. Cursor Configuration

* MCP server configured in Cursor's settings
* Environment variables set for ICAET_API_KEY and USER_EMAIL
* Server starts automatically when Cursor launches
* Server stops gracefully when Cursor closes

## 4. Tool Interface

* Tool name: `query`
* Input parameter: `question` (string, required)
* Returns: ICAET API response (JSON)
* Error handling for missing/invalid parameters

## 5. Security

* No credentials hardcoded in code
* API key and email read from environment variables only
* No sensitive data logged
* All communication with ICAET API over HTTPS

## 6. User Experience

* Developer configures once, uses indefinitely
* Natural language queries work seamlessly
* Multi-turn conversations supported
* Clear error messages for configuration issues
* Helpful prompts guide usage

## 7. Non-Impact to Existing Infrastructure

* Existing ICAET API unchanged and still functional independently
* No AWS resources created or modified
* No dependencies on existing infrastructure
* Can be installed/removed without affecting other systems

## 8. Testing and Quality

* Mock ICAET API server implemented for testing
* Unit tests cover tool logic (>80% coverage)
* Integration tests verify full request/response flow
* Error scenarios tested (401, 404, 500, timeout)
* Tests can run without real ICAET credentials

## 9. Logging and Observability

* Async structured logging implemented with configurable levels
* Logs written to stderr (not stdout)
* Sensitive data properly sanitized in logs
* Optional log file output to `~/.icsaet-mcp/logs/`
* `ICAET_LOG_LEVEL` environment variable supported

---

# Definition of Done

## Functional DoD

* MCP server successfully connects to Cursor
* Queries return ICAET results
* Missing credentials show clear error messages
* Multi-turn conversations work seamlessly
* Prompts display correctly in Cursor

## Security DoD

* No credentials in code
* HTTPS communication with ICAET API
* No sensitive data logged
* Environment variables properly isolated

## Operational DoD

* Simple installation process (pip install + config)
* Clear documentation for setup
* MCP server starts/stops cleanly
* End-to-end test passes
* Troubleshooting guide available
* Mock server available for testing and development
* Test suite passes without real credentials
* Logging configured and documented
* Log files don't contain sensitive data
* Troubleshooting guide includes log file locations and debug mode instructions

---

# Implementation Details

## Technology Stack

* **Language:** Python 3.12+
* **Framework:** fastmcp
* **IDE Integration:** Cursor MCP client
* **Authentication:** Environment variables
* **Deployment:** Local process

## Testing Strategy

### Mock ICAET API Server

For testing purposes, implement a lightweight mock HTTP server that simulates the ICAET API.

**Mock Server Features:**
* Responds to `POST /query` endpoint
* Validates `x-api-key` header and request body structure
* Returns predefined responses for known test questions
* Returns appropriate error codes for invalid requests
* Used via pytest fixture only (not standalone)

**Mock Server Implementation:**
* Simple Flask app in `tests/mock_server.py`
* Uses same request/response format as real ICAET API
* Basic test responses - single test case sufficient

**Testing Approach:**
* **Unit tests**: Mock httpx client, test tool logic in isolation
* **Integration tests**: Use mock server to test full request/response flow
* **Error scenario tests**: Test timeout, 401 (invalid key), 500 (server error) responses

## Logging Configuration

### Basic Async Logging

**Log Levels:**
* `ERROR`: API failures, invalid configurations, network errors
* `WARNING`: Missing optional configurations
* `INFO`: Query requests (sanitized), successful responses
* `DEBUG`: Detailed request/response data (sanitized)

**Log Output:**
* Write to `stderr` (stdout reserved for MCP protocol communication)
* Optional log file: `~/.icsaet-mcp/logs/server.log`
* Human-readable format
* Async logging to avoid blocking I/O

**Environment Variable:**
* `ICAET_LOG_LEVEL`: Set to `DEBUG`, `INFO`, `WARNING`, or `ERROR` (default: `INFO`)

**What to Log:**
```python
# DO LOG:
logger.info("Query received", extra={"question_length": len(question)})
logger.info("API request successful", extra={"status_code": 200})
logger.error("API request failed", extra={"status_code": 401})

# DO NOT LOG:
# - Full API keys (mask: "sk-***abc123")
# - Full email addresses (mask: "u***@example.com")
# - Complete question text at INFO level (only at DEBUG)
```

**Security Considerations:**
* Sanitize all PII before logging
* Mask API keys: Show first 3 and last 6 characters only
* Mask emails: Show first letter and domain only
* Never log full credentials or sensitive query content at INFO/WARNING/ERROR levels

## Cursor MCP Configuration Example

```json
{
  "mcpServers": {
    "icsaet": {
      "command": "python",
      "args": ["-m", "icsaet_mcp"],
      "env": {
        "ICAET_API_KEY": "your-api-key-here",
        "USER_EMAIL": "your-email@example.com"
      }
    }
  }
}
```

## MCP Server Structure

```
icsaet-mcp/
├── pyproject.toml          # Python package configuration
├── README.md               # Setup and usage instructions
├── src/
│   └── icsaet_mcp/
│       ├── __init__.py
│       ├── __main__.py     # MCP server entry point
│       ├── server.py       # fastmcp server implementation
│       ├── tools.py        # Query tool implementation
│       ├── prompts.py      # Prompt templates
│       ├── logging_config.py    # Async logging setup
│       └── utils.py        # Sanitization helpers
└── tests/
    ├── __init__.py
    ├── conftest.py         # Pytest fixtures (mock server)
    ├── mock_server.py      # Basic mock ICAET API
    ├── test_server.py      # Basic tests
    ├── test_tools.py       # Unit tests
    └── test_integration.py # Integration tests
```

## Existing ICAET API Contract

```bash
curl -X POST "https://icaet-dev.wesleyreisz.com/query" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $ICAET_API_KEY" \
  -d '{
    "email": "user@example.com",
    "question": "What stories did Leslie Miley tell in his talk?"
  }'
```

## Installation Steps

1. Install Python package from GitHub: `pip install git+https://github.com/yourusername/icsaet-mcp.git`
    * Alternative: Install from PyPI: `pip install icsaet-mcp` (if published)
2. Configure Cursor MCP settings with API key and email
3. Restart Cursor
4. MCP server starts automatically

See the "Packaging and Distribution" section below for detailed installation options.

## Required Environment Variables

* `ICAET_API_KEY` - API key for ICAET service (required)
* `USER_EMAIL` - Email address to pass to ICAET API (required)

## Optional Environment Variables

* `ICAET_LOG_LEVEL` - Logging level: `DEBUG`, `INFO`, `WARNING`, or `ERROR` (default: `INFO`)

---

# Packaging and Distribution

## Package Configuration (pyproject.toml)

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "icsaet-mcp"
version = "0.1.0"
description = "MCP server for querying the ICAET knowledge base from Cursor IDE"
readme = "README.md"
requires-python = ">=3.12"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
keywords = ["mcp", "cursor", "icaet", "knowledge-base"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
]

dependencies = [
    "fastmcp>=0.1.0",
    "httpx>=0.24.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "pytest-httpx>=0.25.0",
    "flask>=3.0.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
]

[project.urls]
Homepage = "https://github.com/yourusername/icsaet-mcp"
Repository = "https://github.com/yourusername/icsaet-mcp"
Issues = "https://github.com/yourusername/icsaet-mcp/issues"

[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools.package-data]
icsaet_mcp = ["py.typed"]
```

## Installation Methods

### Method 1: Install from GitHub (Recommended for Users)

```bash
pip install git+https://github.com/yourusername/icsaet-mcp.git
```

### Method 2: Install Specific Version/Branch/Tag

```bash
# Install specific tag/version
pip install git+https://github.com/yourusername/icsaet-mcp.git@v0.1.0

# Install specific branch
pip install git+https://github.com/yourusername/icsaet-mcp.git@main

# Install specific commit
pip install git+https://github.com/yourusername/icsaet-mcp.git@abc123def
```

### Method 3: Development Installation (For Contributors)

```bash
# Clone repository
git clone https://github.com/yourusername/icsaet-mcp.git
cd icsaet-mcp

# Install in editable mode with dev dependencies
pip install -e ".[dev]"
```

### Method 4: Install from PyPI (Future Option)

```bash
pip install icsaet-mcp
```

## GitHub Repository Setup

### Required Files

1. **LICENSE** - MIT or Apache 2.0 recommended
2. **README.md** - Installation and usage instructions
3. **pyproject.toml** - Package configuration (shown above)
4. **.gitignore** - Python-specific ignores
5. **MANIFEST.in** - Include non-Python files if needed

### README.md Structure

```markdown
# ICAET MCP Server

MCP server for querying the ICAET knowledge base from Cursor IDE.

## Installation

pip install git+https://github.com/yourusername/icsaet-mcp.git

## Configuration

Add to your Cursor MCP settings (~/.cursor/config.json):

[Configuration JSON example from above]

## Usage

[Usage examples]

## Development

[Development setup instructions]

## License

MIT
```

### GitHub Release Process

1. **Tag Version**
    ```bash
    git tag -a v0.1.0 -m "Release version 0.1.0"
    git push origin v0.1.0
    ```
2. **Create GitHub Release**
    * Go to repository → Releases → Create new release
    * Select the version tag
    * Add release notes
    * Attach built wheel/sdist (optional)
3. **Build Distribution (Optional)**
    ```bash
    pip install build
    python -m build
    ```
    This creates `dist/icsaet_mcp-0.1.0.tar.gz` and `dist/icsaet_mcp-0.1.0-py3-none-any.whl`

## Publishing to PyPI (Optional)

### Test PyPI (Recommended First)

```bash
# Install twine
pip install twine

# Upload to Test PyPI
python -m twine upload --repository testpypi dist/*

# Test installation
pip install --index-url https://test.pypi.org/simple/ icsaet-mcp
```

### Production PyPI

```bash
# Upload to PyPI
python -m twine upload dist/*

# Users can now install via
pip install icsaet-mcp
```

## CI/CD Considerations

### GitHub Actions Example (.github/workflows/release.yml)

```yaml
name: Release

on:
  release:
    types: [published]

jobs:
  build-and-publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Build package
        run: |
          pip install build
          python -m build
      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          password: ${{ secrets.PYPI_API_TOKEN }}
```

## Version Management

* Follow Semantic Versioning (http://semver.org)
* Update version in `pyproject.toml` before release
* Keep CHANGELOG.md updated
* Tag releases in Git

---

# Key Simplifications

* **No OAuth** - Simple environment variable configuration
* **No AWS Infrastructure** - Runs entirely locally
* **No Token Management** - Static API key
* **No Web Server** - MCP protocol over stdio
* **No Database** - Stateless tool calls

---

# Out of Scope

* GitHub OAuth integration (use environment variables instead)
* AWS infrastructure deployment
* Token management or rotation
* Rate limiting (handled by ICAET API if needed)
* User management (single user per configuration)
* Session storage (stateless)
* Multi-user support
* Web-based authentication flows

---

# Prompt Templates (To Be Completed)

## ICAET Overview Prompt

\[STUB: Add description of what ICAET is, what it contains, and how to use it\]

## Example Questions Prompt

\[STUB: Add example questions that demonstrate ICAET capabilities\]

Example format:

* "What did Leslie Miley talk about?"
* \[Add more examples\]

## Question Formatting Guidance Prompt

\[STUB: Add guidance on how to format questions for best results\]

Example guidance:

* Be specific in your questions
* \[Add more formatting tips\]

---

## Issue Links

None

## Latest Comments

No comments

## Technical Considerations

* MCP server runs as a local Python process
* Communication over stdio (not HTTP)
* Stateless design for simplicity
* Minimal dependencies (fastmcp, httpx)
* Async logging to avoid blocking I/O operations
* Mock server for testing without real credentials
* All sensitive data sanitized before logging

---

## Related Issues/Dependencies

* Blockers: None
* Depends on: None
* Related: None

