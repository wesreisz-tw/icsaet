# Task 02: Core MCP Server Implementation

## Story Reference
- **Parent Story:** SCRUM-5 - Cursor MCP Server for ICAET Query Access
- **Task Sequence:** 2 of 8

## Task Objective
Implement the core MCP server using fastmcp framework with proper initialization, configuration, and entry point to enable Cursor IDE integration.

## Scope
- Implement fastmcp server initialization in server.py
- Configure server to read environment variables (ICAET_API_KEY, USER_EMAIL)
- Implement __main__.py entry point for stdio communication
- Add basic server lifecycle management
- Validate required environment variables at startup

## Acceptance Criteria
1. server.py implements fastmcp server:
   - Creates FastMCP instance
   - Reads ICAET_API_KEY and USER_EMAIL from environment
   - Validates required environment variables exist
   - Raises clear error if credentials missing
   - Server instance is importable

2. __main__.py implements entry point:
   - Imports server from server.py
   - Runs server via stdio (fastmcp standard pattern)
   - Handles startup errors gracefully
   - Exits cleanly on shutdown

3. Environment variable validation:
   - Clear error message if ICAET_API_KEY missing
   - Clear error message if USER_EMAIL missing
   - Error messages written to stderr (not stdout)

4. Server can be started manually:
   ```bash
   ICAET_API_KEY=test USER_EMAIL=test@example.com python -m icsaet_mcp
   ```
   - Server starts without errors
   - Server outputs MCP protocol initialization
   - Server waits for stdin input (MCP protocol)

5. Server fails gracefully without credentials:
   ```bash
   python -m icsaet_mcp
   ```
   - Exits with error code 1
   - Shows clear error message on stderr
   - Does not start MCP server

## Dependencies
- **Task 01:** Project structure and dependencies installed

## Required Inputs
- Completed project structure from Task 01
- pyproject.toml with fastmcp dependency
- Stub server.py and __main__.py files

## Expected Outputs and Handoff Criteria

### Outputs
1. Functional server.py with FastMCP instance
2. Functional __main__.py entry point
3. Environment variable validation logic
4. Server lifecycle management (start/stop)

### Handoff Criteria
- Server starts successfully with valid credentials
- Server fails with clear error message without credentials
- `python -m icsaet_mcp` executes without import errors when credentials provided
- Server properly initializes MCP protocol over stdio
- Cursor IDE can connect to server (even if no tools registered yet)

### Handoff to Task 03
- Task 03 will implement the query tool and register it with the server
- Task 03 requires: working MCP server, environment variable access, server instance to register tools with

## Task-Specific Constraints
1. Use fastmcp framework exclusively (no custom MCP protocol implementation)
2. Communication must be over stdio (not HTTP)
3. All errors to stderr, MCP protocol to stdout
4. No hardcoded credentials
5. Server must be stateless (no session storage)
6. No logging implementation yet (Task 04)
7. No tools registered yet (Task 03)

## Implementation Notes
- Follow fastmcp documentation for server initialization
- Use os.getenv() for environment variable access
- Validate credentials before starting server
- Keep server initialization simple and focused

## Validation Checklist
- [ ] server.py creates FastMCP instance
- [ ] Environment variables read correctly
- [ ] Validation errors go to stderr
- [ ] Server starts with valid credentials
- [ ] Server fails without credentials
- [ ] __main__.py runs server via stdio
- [ ] MCP protocol initialization visible in output
