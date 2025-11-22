# Task 03: Query Tool Implementation

## Story Reference
- **Parent Story:** SCRUM-5 - Cursor MCP Server for ICAET Query Access
- **Task Sequence:** 3 of 8

## Task Objective
Implement the query tool that accepts questions and calls the ICAET API, returning results to Cursor IDE through the MCP protocol.

## Scope
- Implement query tool in tools.py
- Register tool with MCP server
- Make HTTP POST requests to ICAET API
- Handle API responses and errors
- Return results in MCP-compatible format

## Acceptance Criteria
1. tools.py implements query function:
   - Decorated with fastmcp tool decorator
   - Accepts `question` parameter (string, required)
   - Uses httpx for async HTTP requests
   - Calls POST https://icaet-dev.wesleyreisz.com/query
   - Sets required headers: Content-Type, x-api-key
   - Sends required body: {email, question}
   - Returns API response as JSON

2. API request format matches specification:
   ```python
   POST https://icaet-dev.wesleyreisz.com/query
   Headers:
     Content-Type: application/json
     x-api-key: {ICAET_API_KEY from env}
   Body:
     {
       "email": "{USER_EMAIL from env}",
       "question": "{user's question}"
     }
   ```

3. Tool registration in server.py:
   - Query tool registered with MCP server
   - Tool discoverable by Cursor IDE
   - Tool metadata includes description and parameter schema

4. Error handling:
   - Network errors return descriptive error message
   - 401 (invalid API key) returns authentication error
   - 404 returns not found error
   - 500 returns server error message
   - Timeout errors return timeout message
   - All errors include status code in response

5. Manual testing possible:
   ```bash
   # With valid credentials, server responds to query requests
   ICAET_API_KEY=real-key USER_EMAIL=real@email.com python -m icsaet_mcp
   # Can send MCP query tool call via stdin
   ```

## Dependencies
- **Task 02:** Working MCP server with environment variable access

## Required Inputs
- Functional server.py with FastMCP instance from Task 02
- Environment variables ICAET_API_KEY and USER_EMAIL accessible
- httpx dependency from Task 01

## Expected Outputs and Handoff Criteria

### Outputs
1. Implemented query tool in tools.py
2. Tool registered with MCP server
3. HTTP client configured for ICAET API
4. Error handling for all API failure modes
5. Tool callable from Cursor IDE

### Handoff Criteria
- Query tool registered and discoverable in MCP server
- Tool successfully calls ICAET API with real credentials
- Tool returns API response in correct format
- Tool handles all error scenarios gracefully
- Tool parameter validation works (question required)
- Cursor IDE can invoke tool and receive responses

### Handoff to Task 04
- Task 04 will add logging to track queries and sanitize sensitive data
- Task 04 requires: working query tool, API request/response flow, error handling paths to log

## Task-Specific Constraints
1. Use httpx for HTTP requests (async compatible)
2. Do not modify ICAET API (read-only integration)
3. HTTPS only (no HTTP fallback)
4. No response caching (stateless)
5. No retry logic (simple implementation)
6. No logging yet (Task 04)
7. Tool description should be helpful but brief

## Implementation Notes
- Use async/await for httpx requests
- Configure reasonable timeout (e.g., 30 seconds)
- Parse JSON responses safely
- Include API error details in error messages
- Keep tool description clear for Cursor users

## API Contract Reference
```bash
curl -X POST "https://icaet-dev.wesleyreisz.com/query" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $ICAET_API_KEY" \
  -d '{
    "email": "user@example.com",
    "question": "What stories did Leslie Miley tell in his talk?"
  }'
```

## Validation Checklist
- [ ] Query tool implemented in tools.py
- [ ] Tool registered with MCP server
- [ ] API request format correct
- [ ] Headers set properly
- [ ] Request body structured correctly
- [ ] Successful responses returned
- [ ] Error scenarios handled
- [ ] Tool discoverable from Cursor
