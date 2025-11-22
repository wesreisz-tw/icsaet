# Task 02 Implementation Plan: Core MCP Server Implementation

## 1. Issue
Implement the core MCP server using fastmcp framework with environment variable configuration and stdio communication to enable Cursor IDE integration. Currently, `server.py` and `__main__.py` are stubs with no functionality.

## 2. Solution
Create a FastMCP server instance in `server.py` that validates required environment variables (`ICAET_API_KEY`, `USER_EMAIL`) at initialization. Implement the `__main__.py` entry point to run the server via stdio communication following the fastmcp standard pattern. Environment validation errors will be written to stderr and cause exit code 1.

**Technical rationale:**
- Use `os.getenv()` for environment variable access (simple, no dependencies)
- Validate credentials before server initialization to fail fast
- Use `sys.stderr.write()` for error messages to keep stdout clean for MCP protocol
- Use `sys.exit(1)` for non-zero exit on validation failures
- Follow fastmcp's `mcp.run()` pattern for stdio-based server execution

## 3. Implementation Steps

1. **Implement environment variable validation in `server.py`:**
   - Import `os` and `sys` modules
   - Read `ICAET_API_KEY` from environment using `os.getenv("ICAET_API_KEY")`
   - Read `USER_EMAIL` from environment using `os.getenv("USER_EMAIL")`
   - If `ICAET_API_KEY` is None or empty string, write "Error: ICAET_API_KEY environment variable is required\n" to `sys.stderr` and call `sys.exit(1)`
   - If `USER_EMAIL` is None or empty string, write "Error: USER_EMAIL environment variable is required\n" to `sys.stderr` and call `sys.exit(1)`

2. **Create FastMCP server instance in `server.py`:**
   - Import `FastMCP` from `fastmcp`
   - After validation, create `mcp = FastMCP("ICAET Query Server")` instance
   - Store validated `ICAET_API_KEY` and `USER_EMAIL` as module-level variables for use by tools in Task 03
   - Export the `mcp` instance (make it importable from this module)

3. **Implement main() function in `__main__.py`:**
   - Import `sys` module
   - Import `mcp` from `.server` module (relative import)
   - Wrap import and server execution in try/except block
   - In try block: call `mcp.run()` to start server via stdio
   - In except block for `SystemExit`: re-raise to preserve exit code
   - In except block for `Exception as e`: write f"Error starting MCP server: {e}\n" to `sys.stderr` and call `sys.exit(1)`

4. **Update module docstrings:**
   - `server.py`: "MCP server implementation with environment variable validation."
   - `__main__.py`: "Entry point for ICAET MCP server."

## 4. Verification

**Manual Testing:**
1. Run `ICAET_API_KEY=test USER_EMAIL=test@example.com python -m icsaet_mcp` - should start without errors and wait for stdin
2. Run `python -m icsaet_mcp` - should exit with code 1 and show "Error: ICAET_API_KEY environment variable is required"
3. Run `ICAET_API_KEY=test python -m icsaet_mcp` - should exit with code 1 and show "Error: USER_EMAIL environment variable is required"

**Key Requirements:**
- Server starts successfully with valid credentials
- Server fails with clear error message without credentials
- All error messages go to stderr, not stdout
- MCP protocol initialization visible when server starts with valid credentials
- Server instance is importable: `python -c "from icsaet_mcp.server import mcp; print('OK')"`
- No import errors when credentials are set

---

## IMPLEMENTATION CHECKLIST

- [ ] Import `os` and `sys` in `server.py`
- [ ] Read `ICAET_API_KEY` environment variable using `os.getenv("ICAET_API_KEY")`
- [ ] Read `USER_EMAIL` environment variable using `os.getenv("USER_EMAIL")`
- [ ] Validate `ICAET_API_KEY` is not None or empty, write error to stderr and exit with code 1 if missing
- [ ] Validate `USER_EMAIL` is not None or empty, write error to stderr and exit with code 1 if missing
- [ ] Import `FastMCP` from `fastmcp` in `server.py`
- [ ] Create `mcp = FastMCP("ICAET Query Server")` instance after validation
- [ ] Store `ICAET_API_KEY` and `USER_EMAIL` as module-level variables in `server.py`
- [ ] Update docstring in `server.py` to "MCP server implementation with environment variable validation."
- [ ] Import `sys` in `__main__.py`
- [ ] Import `mcp` from `.server` using relative import in `__main__.py`
- [ ] Wrap server execution in try/except block in `main()` function
- [ ] Call `mcp.run()` in try block
- [ ] Add except block for `SystemExit` that re-raises
- [ ] Add except block for `Exception` that writes error to stderr and exits with code 1
- [ ] Update docstring in `__main__.py` to "Entry point for ICAET MCP server."
- [ ] Test: Server starts with valid credentials (`ICAET_API_KEY=test USER_EMAIL=test@example.com python -m icsaet_mcp`)
- [ ] Test: Server fails without `ICAET_API_KEY` with proper error message
- [ ] Test: Server fails without `USER_EMAIL` with proper error message
- [ ] Test: Server instance is importable (`python -c "from icsaet_mcp.server import mcp"`)

