# Task 07: Unit and Integration Tests

## Story Reference
- **Parent Story:** SCRUM-5 - Cursor MCP Server for ICAET Query Access
- **Task Sequence:** 7 of 8

## Task Objective
Implement comprehensive unit and integration tests covering tool logic, error handling, API integration, and server lifecycle to achieve >80% code coverage and validate all acceptance criteria.

## Scope
- Implement unit tests for query tool in test_tools.py
- Implement server lifecycle tests in test_server.py
- Implement integration tests in test_integration.py
- Cover all error scenarios (401, 400, 500, timeout, network errors)
- Achieve >80% code coverage
- Validate all SCRUM-5 acceptance criteria through tests

## Acceptance Criteria
1. test_tools.py implements unit tests:
   - Query tool with valid request → success
   - Query tool with missing question → validation error
   - API returns 401 → authentication error
   - API returns 500 → server error
   - Network timeout → timeout error
   - Response parsing success
   - All tests use httpx mocking (no real server)
   - Code coverage >80% for tools.py

2. test_server.py implements server tests:
   - Server starts with valid credentials
   - Server fails with missing ICAET_API_KEY
   - Server fails with missing USER_EMAIL
   - Environment variable reading correct
   - Error messages go to stderr
   - Tool registration successful
   - Prompt registration successful (if implemented)

3. test_integration.py implements end-to-end tests:
   - Full query flow: Cursor → MCP server → Mock API → Response
   - Successful query with mock server
   - Error handling with mock server
   - Multi-step conversation simulation
   - Uses mock server fixture from Task 06
   - Tests full request/response cycle

4. Error scenario coverage:
   - 401 Unauthorized (invalid API key)
   - 400 Bad Request (malformed request)
   - 404 Not Found
   - 500 Internal Server Error
   - Network timeout
   - Connection refused
   - Invalid JSON response

5. Test organization and quality:
   - Tests follow AAA pattern (Arrange, Act, Assert)
   - Descriptive test names
   - One assertion per test (where reasonable)
   - No test interdependencies
   - Fast execution (<5 seconds total)
   - No flaky tests

6. Test execution:
   - All tests pass: `pytest`
   - Coverage report: `pytest --cov=icsaet_mcp --cov-report=term`
   - Coverage >80%
   - No warnings or errors
   - Tests run without real credentials

7. Logging tests:
   - Verify sanitization functions work correctly
   - Verify sensitive data not in logs
   - Verify log levels work as expected
   - Verify log output goes to stderr

## Dependencies
- **Task 06:** Mock server and pytest fixtures
- **Task 03:** Query tool implementation
- **Task 02:** Server implementation
- **Task 04:** Logging implementation

## Required Inputs
- Mock server and fixtures from Task 06
- Working query tool from Task 03
- Working server from Task 02
- Logging system from Task 04
- SCRUM-5 acceptance criteria for validation

## Expected Outputs and Handoff Criteria

### Outputs
1. Comprehensive test_tools.py with unit tests
2. Complete test_server.py with server tests
3. End-to-end test_integration.py
4. >80% code coverage achieved
5. All tests passing
6. No real credentials required for tests

### Handoff Criteria
- `pytest` runs all tests successfully
- Code coverage >80%
- All error scenarios tested
- Integration tests use mock server
- Unit tests use httpx mocking
- Tests run offline without real API
- No flaky or intermittent failures
- Fast test execution (<5 seconds)
- All acceptance criteria validated

### Handoff to Task 08
- Task 08 will create documentation and packaging
- Task 08 requires: working, tested implementation; all features validated; confidence in production readiness

## Task-Specific Constraints
1. No tests call real ICAET API
2. Tests must be fast (<5 seconds total)
3. No external dependencies during tests
4. Tests isolated from each other
5. Use AAA pattern for clarity
6. Mock all network calls
7. Environment variables isolated per test
8. No hardcoded credentials in tests

## Test Structure Example

```python
# test_tools.py
def test_query_successful_response(httpx_mock):
    # Arrange
    httpx_mock.add_response(
        method="POST",
        url="https://icaet-dev.wesleyreisz.com/query",
        json={"answer": "Test answer", "sources": []},
        status_code=200
    )
    
    # Act
    result = query_tool("What is ICAET?")
    
    # Assert
    assert result["answer"] == "Test answer"

def test_query_unauthorized(httpx_mock):
    # Arrange
    httpx_mock.add_response(
        method="POST",
        url="https://icaet-dev.wesleyreisz.com/query",
        status_code=401
    )
    
    # Act & Assert
    with pytest.raises(AuthenticationError):
        query_tool("test question")
```

## Coverage Requirements
- tools.py: >80%
- server.py: >80%
- logging_config.py: >70%
- utils.py: >90% (simple sanitization functions)
- prompts.py: >60% (static content)

## Validation Checklist
- [ ] test_tools.py implemented
- [ ] test_server.py implemented
- [ ] test_integration.py implemented
- [ ] All error scenarios covered
- [ ] Code coverage >80%
- [ ] All tests pass
- [ ] Tests use mock server
- [ ] No real API calls
- [ ] Fast execution
- [ ] AAA pattern followed
- [ ] Logging tests included
- [ ] Sanitization tests included
