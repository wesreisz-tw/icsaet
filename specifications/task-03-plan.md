# Task 03 Implementation Plan: Query Tool Implementation

## 1. Issue
Implement the query tool in `tools.py` that accepts questions from Cursor IDE, calls the ICAET API via POST request, and returns results through the MCP protocol. Currently `tools.py` contains only a stub with no functionality.

## 2. Solution
Create an async `query` function decorated with `@mcp.tool()` that accepts a `question` parameter, makes an HTTP POST request to the ICAET API using httpx with proper headers and authentication, handles errors gracefully, and returns the API response. Register this tool with the existing FastMCP server instance in `server.py`.

**Technical rationale:**
- Use `httpx.AsyncClient` for async HTTP requests (compatible with fastmcp)
- Import environment variables from `server.py` (already validated)
- Use 30-second timeout for API requests (reasonable default)
- Handle HTTP errors with descriptive messages including status codes
- Parse JSON responses safely with try/except
- Return raw API response as dict (MCP will serialize to JSON)

## 3. Implementation Steps

1. **Implement query function in `tools.py`:**
   - Import `httpx` module
   - Import `mcp`, `ICAET_API_KEY`, `USER_EMAIL` from `.server` using relative import
   - Create async function `query(question: str) -> dict`
   - Add `@mcp.tool()` decorator with description: "Query the ICAET knowledge base with a question"
   - Add docstring explaining the function parameters and return value

2. **Implement HTTP request logic in query function:**
   - Create `url = "https://icaet-dev.wesleyreisz.com/query"`
   - Create `headers` dict with `"Content-Type": "application/json"` and `"x-api-key": ICAET_API_KEY`
   - Create `body` dict with `"email": USER_EMAIL` and `"question": question`
   - Wrap in try/except for `httpx.HTTPStatusError`, `httpx.RequestError`, and general `Exception`

3. **Implement API call with error handling:**
   - In try block: use `async with httpx.AsyncClient(timeout=30.0) as client:`
   - Call `response = await client.post(url, json=body, headers=headers)`
   - Call `response.raise_for_status()` to raise errors for 4xx/5xx status codes
   - Parse and return `response.json()`
   - In `httpx.HTTPStatusError` except block: return dict with `"error"` key containing f"API error {e.response.status_code}: {e.response.text}"
   - In `httpx.RequestError` except block: return dict with `"error"` key containing f"Request failed: {str(e)}"
   - In general `Exception` except block: return dict with `"error"` key containing f"Unexpected error: {str(e)}"

4. **Update module docstring:**
   - Change `tools.py` docstring to: "MCP tools for ICAET query operations."
   - Remove `pass` statement

## 4. Verification

**Manual Testing:**
1. Run `ICAET_API_KEY=real-key USER_EMAIL=real@email.com python -m icsaet_mcp` - server should start
2. Send MCP query tool call via stdin (if MCP inspector available)
3. Verify tool is discoverable in Cursor IDE MCP tools list
4. Test with valid question - should return API response
5. Test with invalid API key - should return 401 error message
6. Test with network timeout - should return timeout error

**Key Requirements:**
- Query tool registered and discoverable via MCP
- Tool accepts `question` parameter (string, required)
- Tool calls POST https://icaet-dev.wesleyreisz.com/query
- Headers include Content-Type and x-api-key
- Body includes email and question
- Successful responses return API JSON
- HTTP errors return descriptive error dict
- Network errors return descriptive error dict
- Tool is callable from Cursor IDE

---

## IMPLEMENTATION CHECKLIST

- [ ] Import `httpx` in `tools.py`
- [ ] Import `mcp`, `ICAET_API_KEY`, `USER_EMAIL` from `.server` in `tools.py`
- [ ] Create async function `query(question: str) -> dict` in `tools.py`
- [ ] Add `@mcp.tool()` decorator with description "Query the ICAET knowledge base with a question"
- [ ] Add function docstring explaining parameters and return value
- [ ] Set `url = "https://icaet-dev.wesleyreisz.com/query"` in function
- [ ] Create `headers` dict with "Content-Type": "application/json" and "x-api-key": ICAET_API_KEY
- [ ] Create `body` dict with "email": USER_EMAIL and "question": question
- [ ] Add try/except blocks for `httpx.HTTPStatusError`, `httpx.RequestError`, and `Exception`
- [ ] Implement `async with httpx.AsyncClient(timeout=30.0) as client:` in try block
- [ ] Call `response = await client.post(url, json=body, headers=headers)` in try block
- [ ] Call `response.raise_for_status()` after POST request
- [ ] Return `response.json()` for successful requests
- [ ] Implement HTTPStatusError handler returning `{"error": f"API error {e.response.status_code}: {e.response.text}"}`
- [ ] Implement RequestError handler returning `{"error": f"Request failed: {str(e)}"}`
- [ ] Implement general Exception handler returning `{"error": f"Unexpected error: {str(e)}"}`
- [ ] Update module docstring to "MCP tools for ICAET query operations."
- [ ] Remove `pass` statement from `tools.py`
- [ ] Test: Server starts with valid credentials
- [ ] Test: Query tool is discoverable in MCP
- [ ] Test: Tool accepts question parameter
- [ ] Test: Tool makes POST request to correct URL
- [ ] Test: Headers are set correctly
- [ ] Test: Request body is structured correctly
- [ ] Test: Successful responses are returned
- [ ] Test: HTTP errors are handled with descriptive messages
- [ ] Test: Network errors are handled gracefully

