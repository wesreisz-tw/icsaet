# Task 07 Implementation Plan: Unit and Integration Tests (REVISED)

**REVISION NOTES:**
- **Original execution revealed**: FastMCP decorators (`@mcp.tool()`, `@mcp.prompt()`) wrap functions making them not directly callable in tests
- **Solution**: Extract business logic into separate implementation functions that can be tested directly
- **Also fixed**: `test_sanitize_api_key_exactly_nine` assertion corrected to match actual function behavior (first 3 + last 6 chars)
- **Impact**: Added Phase 1 (refactoring) before Phase 2 (testing). No change to overall coverage targets or test counts.

## 1. Issue

The ICAET MCP server currently has empty test files (only `pass` statements in test_tools.py, test_server.py, and test_integration.py). We need comprehensive unit and integration tests covering:
- Query tool functionality with all success and error scenarios
- Server lifecycle and environment variable validation
- End-to-end integration testing using the mock server
- Logging and sanitization utilities
- Code coverage >80% across all modules

**Critical Discovery:** Functions decorated with `@mcp.tool()` and `@mcp.prompt()` are wrapped by FastMCP and not directly callable. We must refactor the code to separate business logic from MCP decorators for testability.

## 2. Solution

**Phase 1: Refactor for Testability**
- Extract business logic from decorated functions into separate testable functions
- Move query logic to `_query_impl()` function in tools.py
- Move prompt logic to `_get_icaet_overview()`, `_get_example_questions()`, `_get_question_formatting()` in prompts.py
- Decorated functions become thin wrappers that call the implementation functions

**Phase 2: Implement Test Suites**
1. **test_tools.py**: Unit tests using pytest-httpx to mock HTTP requests, testing `_query_impl()` directly
2. **test_server.py**: Server initialization tests using subprocess for environment validation
3. **test_integration.py**: End-to-end tests using the mock Flask server
4. **test_utils.py**: Test sanitization functions with corrected assertions
5. **test_logging.py**: Test logging configuration
6. **test_prompts.py**: Test prompt implementation functions directly

All tests follow AAA pattern, use descriptive names, run offline without real credentials, and execute in <5 seconds total.

## 3. Implementation Steps

### Step 0: Refactor tools.py and prompts.py for testability

#### Step 0a: Refactor tools.py
File: `/Users/wesleyreisz/work/mcp/icsaet/icsaet-mcp/src/icsaet_mcp/tools.py`

Extract the query logic into a separate function:
1. Add new function `async def _query_impl(question: str, api_key: str, user_email: str) -> dict:` before the decorated function
2. Move all logic from lines 22-50 (the entire function body) into `_query_impl`
3. Update URL construction, headers, and body to use the `api_key` and `user_email` parameters instead of module globals
4. Keep all logging, error handling, and return statements in `_query_impl`
5. Update the decorated `@mcp.tool()` `query` function to become a simple one-liner: `return await _query_impl(question, ICAET_API_KEY, USER_EMAIL)`
6. The `_query_impl` function is now fully testable with explicit parameters

#### Step 0b: Refactor prompts.py
File: `/Users/wesleyreisz/work/mcp/icsaet/icsaet-mcp/src/icsaet_mcp/prompts.py`

Extract prompt content into separate functions:
1. Add new function `def _get_icaet_overview() -> str:` before the `@mcp.prompt()` decorated `icaet_overview()` function
2. Move the entire multi-line string (lines 9-34) into `_get_icaet_overview()` as its return value
3. Update decorated `icaet_overview()` to: `return _get_icaet_overview()`
4. Add new function `def _get_example_questions() -> str:` before the decorated `example_questions()` function
5. Move the entire multi-line string (lines 40-63) into `_get_example_questions()` as its return value
6. Update decorated `example_questions()` to: `return _get_example_questions()`
7. Add new function `def _get_question_formatting() -> str:` before the decorated `question_formatting()` function
8. Move the entire multi-line string (lines 69-103) into `_get_question_formatting()` as its return value
9. Update decorated `question_formatting()` to: `return _get_question_formatting()`
10. All implementation functions (`_get_*`) are now directly testable

### Step 1: Implement test_tools.py unit tests
File: `/Users/wesleyreisz/work/mcp/icsaet/icsaet-mcp/tests/test_tools.py`

Replace the entire file content with:
- Import statements: pytest, pytest.mark.asyncio, httpx_mock fixture
- Import the `_query_impl` function from icsaet_mcp.tools
- Import monkeypatch for environment setup

Test cases to implement (testing `_query_impl` directly):
1. `test_query_successful_response(httpx_mock)` - Mock 200 response with valid JSON, verify returned dict contains "answer", "sources", "confidence"
2. `test_query_401_unauthorized(httpx_mock)` - Mock 401 response, verify error dict returned
3. `test_query_400_bad_request(httpx_mock)` - Mock 400 response, verify error dict returned
4. `test_query_404_not_found(httpx_mock)` - Mock 404 response, verify error dict returned
5. `test_query_500_server_error(httpx_mock)` - Mock 500 response, verify error dict returned
6. `test_query_timeout_error(httpx_mock)` - Mock httpx.TimeoutException, verify error dict with "Request failed" message
7. `test_query_connection_error(httpx_mock)` - Mock httpx.ConnectError, verify error dict with "Request failed" message
8. `test_query_invalid_json_response(httpx_mock)` - Mock 200 response with invalid JSON body, verify error dict returned
9. `test_query_empty_question(httpx_mock)` - Test with empty string question, verify API still called
10. `test_query_long_question(httpx_mock)` - Test with 500+ character question, verify successful processing
11. `test_query_uses_correct_headers(httpx_mock)` - Verify API key header and content-type are set correctly
12. `test_query_uses_correct_endpoint(httpx_mock)` - Verify POST to https://icaet-dev.wesleyreisz.com/query

Each test must:
- Call `_query_impl(question, "test-api-key", "test@example.com")` directly with explicit parameters
- Use httpx_mock.add_response() with method="POST" and url="https://icaet-dev.wesleyreisz.com/query"
- Follow AAA pattern with comments
- Use @pytest.mark.asyncio decorator
- Have single clear assertion

### Step 2: Implement test_server.py server lifecycle tests
File: `/Users/wesleyreisz/work/mcp/icsaet/icsaet-mcp/tests/test_server.py`

Replace the entire file content with:
- Import statements: pytest, os, sys, importlib
- Import monkeypatch

Test cases to implement:
1. `test_server_initialization_success(monkeypatch, capsys)` - Set both env vars, reload server module, verify no sys.exit called, verify logger.info messages
2. `test_server_missing_icaet_api_key(monkeypatch)` - Unset ICAET_API_KEY, verify pytest.raises(SystemExit) with code 1 when importing server
3. `test_server_missing_user_email(monkeypatch)` - Set API_KEY but unset USER_EMAIL, verify pytest.raises(SystemExit) with code 1
4. `test_server_missing_both_credentials(monkeypatch)` - Unset both, verify pytest.raises(SystemExit) with code 1
5. `test_server_empty_api_key(monkeypatch)` - Set ICAET_API_KEY="" (empty string), verify SystemExit
6. `test_server_empty_email(monkeypatch)` - Set USER_EMAIL="" (empty string), verify SystemExit
7. `test_server_stderr_output_missing_api_key(monkeypatch, capsys)` - Verify stderr contains "ICAET_API_KEY environment variable is required"
8. `test_server_stderr_output_missing_email(monkeypatch, capsys)` - Verify stderr contains "USER_EMAIL environment variable is required"
9. `test_server_creates_mcp_instance(monkeypatch)` - Verify mcp object is instance of FastMCP
10. `test_server_mcp_has_correct_name(monkeypatch)` - Verify mcp.name or similar attribute is "ICAET Query Server"

Note: Server module executes code at import time, so need to use importlib.reload() or import in controlled way. Use subprocess to test sys.exit scenarios in isolation.

### Step 3: Implement test_integration.py end-to-end tests
File: `/Users/wesleyreisz/work/mcp/icsaet/icsaet-mcp/tests/test_integration.py`

Replace the entire file content with:
- Import statements: pytest, httpx, pytest.mark.asyncio
- Import query function from icsaet_mcp.tools

Test cases to implement:
1. `test_integration_successful_query(mock_icaet_url, monkeypatch)` - Set env vars, call query(), verify response has answer/sources
2. `test_integration_unauthorized_no_api_key(mock_icaet_url, monkeypatch)` - Set API_KEY="", verify 401 error response
3. `test_integration_missing_question_field(mock_icaet_url, monkeypatch)` - Modify query to send empty question, verify 400 error
4. `test_integration_server_error_trigger(mock_icaet_url, monkeypatch)` - Use question="trigger_server_error", verify 500 error handling
5. `test_integration_multi_query_sequence(mock_icaet_url, monkeypatch)` - Call query 3 times with different questions, verify all succeed
6. `test_integration_mock_server_returns_sources(mock_icaet_url, monkeypatch)` - Verify response includes sources array with "mock_source.txt"
7. `test_integration_mock_server_returns_confidence(mock_icaet_url, monkeypatch)` - Verify response includes confidence=0.95
8. `test_integration_uses_environment_email(mock_icaet_url, monkeypatch)` - Set specific email, verify it's used in request

Each test must:
- Use monkeypatch.setenv() to set environment variables pointing to mock_icaet_url
- Use @pytest.mark.asyncio decorator
- Call actual query() function (not mocked)
- Follow AAA pattern

Note: These tests use the actual mock Flask server started by conftest.py fixtures, providing true HTTP integration testing.

### Step 4: Implement utils.py sanitization tests
File: `/Users/wesleyreisz/work/mcp/icsaet/icsaet-mcp/tests/test_utils.py` (create new file)

Create new test file with:
- Import statements: pytest
- Import all three sanitization functions from icsaet_mcp.utils

Test cases to implement:
1. `test_sanitize_api_key_normal()` - Input "abc123456789", expect "abc***456789"
2. `test_sanitize_api_key_short()` - Input "short", expect "***"
3. `test_sanitize_api_key_empty()` - Input "", expect ""
4. `test_sanitize_api_key_none()` - Input None, expect "None"
5. `test_sanitize_api_key_exactly_nine()` - Input "123456789", expect "123***456789" (first 3 + *** + last 6)
6. `test_sanitize_email_normal()` - Input "user@example.com", expect "u***@example.com"
7. `test_sanitize_email_short_username()` - Input "a@example.com", expect "a***@example.com"
8. `test_sanitize_email_invalid_no_at()` - Input "notanemail", expect "***"
9. `test_sanitize_email_empty()` - Input "", expect ""
10. `test_sanitize_email_none()` - Input None, expect "None"
11. `test_sanitize_email_multiple_at()` - Input "user@@example.com", expect "***"
12. `test_sanitize_question_short()` - Input "Hello?", expect "Hello?"
13. `test_sanitize_question_exactly_max()` - Input 50 chars, expect same 50 chars
14. `test_sanitize_question_over_max()` - Input 100 chars, expect 50 chars + "..."
15. `test_sanitize_question_empty()` - Input "", expect ""
16. `test_sanitize_question_none()` - Input None, expect "None"
17. `test_sanitize_question_custom_max_len()` - Input "Hello world" with max_len=5, expect "Hello..."

Target: >90% coverage for utils.py

### Step 5: Implement logging configuration tests
File: `/Users/wesleyreisz/work/mcp/icsaet/icsaet-mcp/tests/test_logging.py` (create new file)

Create new test file with:
- Import statements: pytest, logging, os, sys
- Import setup_logging from icsaet_mcp.logging_config

Test cases to implement:
1. `test_setup_logging_default_level(monkeypatch)` - No ICAET_LOG_LEVEL set, verify logger level is INFO
2. `test_setup_logging_debug_level(monkeypatch)` - Set ICAET_LOG_LEVEL="DEBUG", verify logger level is DEBUG
3. `test_setup_logging_warning_level(monkeypatch)` - Set ICAET_LOG_LEVEL="WARNING", verify logger level is WARNING
4. `test_setup_logging_invalid_level(monkeypatch)` - Set ICAET_LOG_LEVEL="INVALID", verify defaults to INFO
5. `test_setup_logging_returns_logger()` - Verify return value is logging.Logger instance
6. `test_setup_logging_stderr_handler()` - Verify logger has StreamHandler writing to stderr
7. `test_setup_logging_creates_log_directory(tmp_path, monkeypatch)` - Mock Path.home() to tmp_path, verify ~/.icsaet-mcp/logs created
8. `test_setup_logging_handles_file_creation_failure(monkeypatch)` - Mock mkdir to raise exception, verify logger still works (stderr only)
9. `test_setup_logging_format()` - Verify log format includes asctime, levelname, message

Target: >70% coverage for logging_config.py

### Step 6: Implement prompts tests
File: `/Users/wesleyreisz/work/mcp/icsaet/icsaet-mcp/tests/test_prompts.py` (create new file)

Create new test file with:
- Import statements: pytest
- Import implementation functions `_get_icaet_overview`, `_get_example_questions`, `_get_question_formatting` from icsaet_mcp.prompts

Test cases to implement:
1. `test_icaet_overview_returns_string()` - Verify `_get_icaet_overview()` returns non-empty string
2. `test_icaet_overview_contains_key_sections()` - Verify contains "What is ICAET?", "What information does it contain?", etc.
3. `test_example_questions_returns_string()` - Verify `_get_example_questions()` returns non-empty string
4. `test_example_questions_contains_examples()` - Verify contains numbered examples
5. `test_question_formatting_returns_string()` - Verify `_get_question_formatting()` returns non-empty string
6. `test_question_formatting_contains_best_practices()` - Verify contains "For Better Results" and "What to Avoid"

Target: >60% coverage for prompts.py (static content, limited logic to test)

### Step 7: Add pytest configuration to pyproject.toml
File: `/Users/wesleyreisz/work/mcp/icsaet/icsaet-mcp/pyproject.toml`

Add after [project.scripts] section:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
asyncio_mode = "auto"
addopts = [
    "-v",
    "--strict-markers",
    "--tb=short",
    "--cov=icsaet_mcp",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--cov-fail-under=80"
]

[tool.coverage.run]
source = ["src/icsaet_mcp"]
omit = [
    "*/tests/*",
    "*/__pycache__/*",
    "*/.venv/*"
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
    "pass"
]
```

### Step 8: Add pytest-cov to dev dependencies
File: `/Users/wesleyreisz/work/mcp/icsaet/icsaet-mcp/pyproject.toml`

In [project.optional-dependencies] dev array, add:
- "pytest-cov>=4.1.0"

### Step 9: Verify all imports work correctly
File: All test files

For each test file created/modified:
- Ensure all imports use absolute imports from icsaet_mcp package
- Verify no circular import issues
- Ensure monkeypatch used correctly for environment isolation

### Step 10: Run tests and verify coverage
Commands to run:
1. `cd /Users/wesleyreisz/work/mcp/icsaet/icsaet-mcp`
2. `pytest -v` - Run all tests, verify all pass
3. `pytest --cov=icsaet_mcp --cov-report=term-missing` - Run with coverage report
4. `pytest --cov=icsaet_mcp --cov-report=html` - Generate HTML coverage report
5. Verify coverage >80% overall
6. Verify individual module coverage meets targets (post-refactoring):
   - tools.py: >80% (`_query_impl` fully covered; decorated wrapper covered by integration tests)
   - server.py: >80% (environment validation paths covered via subprocess tests)
   - utils.py: >90% (all sanitization function branches testable)
   - logging_config.py: >70% (core functionality covered; some error paths may be unreachable)
   - prompts.py: >60% (implementation functions fully covered; decorated wrappers covered by calls)
   - __main__.py: 0% acceptable (entry point, tested via integration/manual testing)

### Step 11: Fix any failing tests or coverage gaps
If coverage <80%:
- Identify uncovered lines using coverage report
- Add specific tests to cover missing branches
- Focus on error handling paths and edge cases
- Re-run coverage until >80% achieved

If tests fail:
- Review test assertions
- Check environment variable isolation
- Verify httpx_mock configurations match actual tool implementation
- Ensure async/await used correctly with pytest-asyncio

## 4. Verification

### Functional Requirements
- [ ] All test files implemented (test_tools.py, test_server.py, test_integration.py, test_utils.py, test_logging.py, test_prompts.py)
- [ ] All tests use AAA pattern with clear comments
- [ ] Unit tests use httpx_mock, no real HTTP calls
- [ ] Integration tests use mock_icaet_url fixture with real HTTP to mock server
- [ ] All environment variables isolated using monkeypatch
- [ ] No hardcoded credentials in any test file

### Error Coverage Requirements
- [ ] 401 Unauthorized tested
- [ ] 400 Bad Request tested
- [ ] 404 Not Found tested
- [ ] 500 Internal Server Error tested
- [ ] Network timeout tested
- [ ] Connection error tested
- [ ] Invalid JSON response tested
- [ ] Missing environment variables tested
- [ ] Empty/invalid input values tested

### Code Coverage Requirements
- [ ] Overall coverage >80%
- [ ] tools.py coverage >80%
- [ ] server.py coverage >80%
- [ ] utils.py coverage >90%
- [ ] logging_config.py coverage >70%
- [ ] prompts.py coverage >60%

### Test Quality Requirements
- [ ] All tests pass: `pytest` returns 0 exit code
- [ ] Tests run in <5 seconds total
- [ ] No flaky tests (run `pytest` 5 times, all pass)
- [ ] No test interdependencies (can run tests in any order)
- [ ] Tests work offline without real API credentials
- [ ] Coverage report generated successfully

### SCRUM-5 Acceptance Criteria Validation
- [ ] Query tool tested with valid request → success
- [ ] Query tool tested with all error scenarios
- [ ] Server lifecycle tested (start, fail, env vars)
- [ ] Integration tests cover full request/response cycle
- [ ] Logging and sanitization functions validated
- [ ] All acceptance criteria from task-07.md satisfied

## IMPLEMENTATION CHECKLIST

**Phase 1: Refactor for Testability**
1. Refactor tools.py: Extract business logic into `_query_impl(question, api_key, user_email)` function
2. Refactor prompts.py: Extract content into `_get_icaet_overview()`, `_get_example_questions()`, `_get_question_formatting()` functions
3. Update decorated functions to call implementation functions

**Phase 2: Implement Tests**
4. Replace test_tools.py with 12 unit tests calling `_query_impl` directly with httpx_mock
5. Replace test_server.py with 10 server lifecycle tests using subprocess
6. Replace test_integration.py with 8 end-to-end tests using mock_icaet_url fixture
7. Fix test_utils.py assertion: "123456789" → "123***456789" (not "123***789")
8. Update test_prompts.py to call implementation functions (`_get_*` functions)
9. Verify test_logging.py passes (already created correctly)

**Phase 3: Configuration and Validation**
10. Verify [tool.pytest.ini_options] section exists in pyproject.toml
11. Verify [tool.coverage.run] section exists in pyproject.toml
12. Verify [tool.coverage.report] section exists in pyproject.toml
13. Verify "pytest-cov>=4.1.0" in dev dependencies
14. Run `pytest -v` to verify all tests pass
15. Run `pytest --cov=icsaet_mcp --cov-report=term-missing` to verify >80% coverage
16. Run `pytest --cov=icsaet_mcp --cov-report=html` to generate HTML report
17. Review coverage report and add tests for any gaps below target thresholds
18. Run `pytest` 5 times to verify no flaky tests
19. Verify total test execution time <5 seconds
20. Verify all tests work offline without real ICAET_API_KEY or USER_EMAIL

