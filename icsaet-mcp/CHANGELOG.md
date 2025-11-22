# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-11-22

### Added
- Initial release of ICAET MCP Server
- MCP (Model Context Protocol) server implementation using fastmcp
- ICAET knowledge base API integration with query support
- Structured logging with configurable log levels (DEBUG, INFO, WARNING, ERROR)
- Environment-based configuration (ICAET_API_KEY, USER_EMAIL, ICAET_LOG_LEVEL)
- Comprehensive error handling for API failures and network issues
- Request timeout handling (30 second default)
- Retry logic for transient failures
- Full test suite with unit and integration tests
- Test coverage reporting (>80% coverage requirement)
- Mock server for integration testing
- Detailed prompt and resource management
- API response validation and error formatting

### Known Limitations
- Requires Python 3.12 or higher
- API rate limiting not implemented (depends on ICAET API limits)
- Single query tool only (no batch queries)
- No caching of API responses
- Requires environment variables for authentication

### Dependencies
- fastmcp >= 0.1.0
- httpx >= 0.24.0
- pytest >= 7.4.0 (dev)
- pytest-asyncio >= 0.21.0 (dev)
- pytest-httpx >= 0.22.0 (dev)
- pytest-cov >= 4.1.0 (dev)

---

**Note:** This project follows [Semantic Versioning](https://semver.org/). Version numbers follow the MAJOR.MINOR.PATCH format where:
- MAJOR version increments indicate incompatible API changes
- MINOR version increments add functionality in a backward compatible manner
- PATCH version increments make backward compatible bug fixes

