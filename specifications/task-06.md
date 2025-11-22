# Task 06: Mock Server and Testing Infrastructure

## Story Reference
- **Parent Story:** SCRUM-5 - Cursor MCP Server for ICAET Query Access
- **Task Sequence:** 6 of 8

## Task Objective
Implement a lightweight mock ICAET API server and pytest infrastructure to enable testing without real credentials, supporting both unit and integration tests.

## Scope
- Implement mock ICAET API server in tests/mock_server.py
- Create pytest fixtures in tests/conftest.py
- Set up test configuration for httpx mocking
- Provide mock responses for common test scenarios
- Enable tests to run completely offline

## Acceptance Criteria
1. mock_server.py implements basic Flask app:
   - Responds to POST /query endpoint
   - Validates x-api-key header presence
   - Validates request body structure (email, question)
   - Returns JSON responses matching ICAET API format
   - Returns appropriate error codes (401, 400, 500)
   - Runs on localhost for testing only

2. Mock server test responses:
   - Valid request → 200 OK with sample answer
   - Missing API key → 401 Unauthorized
   - Invalid JSON → 400 Bad Request
   - Server error scenario → 500 Internal Server Error
   - At least one realistic test response for a known question

3. conftest.py implements pytest fixtures:
   - `mock_icaet_server`: Starts/stops mock Flask server
   - `mock_icaet_url`: Provides mock server URL
   - `valid_credentials`: Provides test API key and email
   - `httpx_mock`: Configures httpx mocking for unit tests
   - Fixtures properly scoped (session, module, function as appropriate)

4. Test environment configuration:
   - Mock server starts on random available port
   - Server cleanup on test completion
   - Environment variables isolated per test
   - No cross-test contamination

5. Mock server usage patterns:
   - Unit tests: Mock httpx client (no server needed)
   - Integration tests: Use running mock server
   - pytest fixtures handle all setup/teardown
   - Tests never call real ICAET API

6. Documentation:
   - Fixture usage documented in conftest.py
   - Mock response format documented
   - Example test using fixtures included

## Dependencies
- **Task 03:** Query tool implementation (defines API contract)
- **Task 02:** Server implementation (to test)
- **Task 01:** Test dependencies installed (pytest, flask, pytest-httpx)

## Required Inputs
- Working query tool from Task 03 (defines expected API contract)
- ICAET API contract from SCRUM-5 specification
- Test dependencies from pyproject.toml (Task 01)

## Expected Outputs and Handoff Criteria

### Outputs
1. Functional mock_server.py with Flask app
2. Comprehensive conftest.py with pytest fixtures
3. Mock responses for common scenarios
4. Test infrastructure ready for test implementation
5. Documentation of fixture usage

### Handoff Criteria
- Mock server can be started via pytest fixture
- Mock server responds to all test scenarios (200, 401, 400, 500)
- Fixtures properly initialize and cleanup
- Tests can run without real ICAET credentials
- httpx mocking configured for unit tests
- Integration test can call mock server successfully
- No network calls to real ICAET API during tests

### Handoff to Task 07
- Task 07 will implement actual unit and integration tests
- Task 07 requires: working mock server, pytest fixtures, test infrastructure, mock response patterns

## Task-Specific Constraints
1. Mock server must match real ICAET API contract
2. Mock server for testing only (not standalone tool)
3. Use pytest fixtures exclusively (no global state)
4. Mock server on random port (avoid conflicts)
5. Keep mock responses simple (basic test cases)
6. No database or persistence (in-memory only)
7. Flask in minimal configuration (testing only)

## Implementation Notes
- Use Flask's test mode for mock server
- pytest-httpx for unit test HTTP mocking
- pytest fixtures for integration test server
- Random port selection: `app.run(port=0)` finds available port
- Proper cleanup in fixture teardown
- Document fixture scope clearly

## Mock Response Examples

### Successful Query
```json
{
  "answer": "Leslie Miley discussed engineering leadership and diversity in tech.",
  "sources": ["transcript_leslie_miley.txt"],
  "confidence": 0.95
}
```

### Error Responses
```json
// 401 Unauthorized
{"error": "Invalid API key"}

// 400 Bad Request
{"error": "Missing required field: question"}

// 500 Internal Server Error
{"error": "Internal server error"}
```

## Validation Checklist
- [ ] mock_server.py implements Flask app
- [ ] POST /query endpoint responds
- [ ] API key validation works
- [ ] Request body validation works
- [ ] Error scenarios return correct codes
- [ ] conftest.py implements all fixtures
- [ ] Fixtures start/stop server correctly
- [ ] httpx mocking configured
- [ ] Tests can run offline
- [ ] No real API calls during tests
- [ ] Fixture usage documented
