# Task 04: Logging System Implementation

## Story Reference
- **Parent Story:** SCRUM-5 - Cursor MCP Server for ICAET Query Access
- **Task Sequence:** 4 of 8

## Task Objective
Implement async structured logging with configurable levels, proper sanitization of sensitive data, and output to stderr and optional log files.

## Scope
- Implement async logging configuration in logging_config.py
- Implement sanitization utilities in utils.py
- Add logging to server startup and query tool
- Configure log levels via ICAET_LOG_LEVEL environment variable
- Set up optional log file output to ~/.icsaet-mcp/logs/

## Acceptance Criteria
1. logging_config.py implements async logging:
   - Configurable log level via ICAET_LOG_LEVEL env var (DEBUG, INFO, WARNING, ERROR)
   - Default log level: INFO
   - Output to stderr (stdout reserved for MCP protocol)
   - Optional file output to ~/.icsaet-mcp/logs/server.log
   - Human-readable format with timestamp, level, message
   - Async logging to avoid blocking I/O

2. utils.py implements sanitization functions:
   - `sanitize_api_key(key: str) -> str`: Shows first 3 and last 6 chars (e.g., "sk-***abc123")
   - `sanitize_email(email: str) -> str`: Shows first char and domain (e.g., "u***@example.com")
   - `sanitize_question(question: str, max_len: int = 50) -> str`: Truncates for INFO level
   - All functions handle None/empty strings gracefully

3. Logging integrated into server.py:
   - INFO: Server starting
   - INFO: Server configuration loaded (sanitized credentials)
   - ERROR: Missing credentials
   - INFO: Server ready

4. Logging integrated into tools.py:
   - INFO: Query received (question_length only)
   - DEBUG: Full question text (sanitized)
   - INFO: API request successful (status_code)
   - ERROR: API request failed (status_code, error type)
   - DEBUG: API response details (sanitized)

5. Log level behavior:
   - ERROR: Only errors logged
   - WARNING: Warnings and errors
   - INFO: Standard operational logs (no sensitive data)
   - DEBUG: Detailed logs with sanitized sensitive data

6. Log output examples:
   ```
   2025-11-22 10:30:15 INFO Server starting
   2025-11-22 10:30:15 INFO Configuration loaded [api_key=sk-***abc123, email=u***@example.com]
   2025-11-22 10:30:16 INFO Server ready
   2025-11-22 10:31:45 INFO Query received [question_length=42]
   2025-11-22 10:31:46 INFO API request successful [status_code=200]
   ```

## Dependencies
- **Task 02:** Working MCP server
- **Task 03:** Working query tool with API integration

## Required Inputs
- Functional server.py from Task 02
- Functional tools.py with query implementation from Task 03
- Environment variable access for ICAET_LOG_LEVEL

## Expected Outputs and Handoff Criteria

### Outputs
1. Async logging configuration in logging_config.py
2. Sanitization utilities in utils.py
3. Logging integrated throughout server and tools
4. Configurable log levels working
5. Log files created in ~/.icsaet-mcp/logs/ (when enabled)

### Handoff Criteria
- Logging works at all levels (DEBUG, INFO, WARNING, ERROR)
- All sensitive data properly sanitized in logs
- Logs output to stderr (not stdout)
- Log file creation optional and functional
- No PII or credentials in INFO/WARNING/ERROR logs
- Server startup, queries, and errors all logged appropriately
- Log format human-readable and consistent

### Handoff to Task 05
- Task 05 will implement MCP prompts for user guidance
- Task 05 requires: working server with logging, error handling patterns to reference

## Task-Specific Constraints
1. All logs to stderr (stdout reserved for MCP protocol)
2. No sensitive data in INFO/WARNING/ERROR levels
3. Async logging to prevent blocking
4. Sanitization must be fail-safe (never raise exceptions)
5. Log file directory created automatically if needed
6. Default to INFO level if ICAET_LOG_LEVEL invalid
7. No external logging services (local only)

## Security Requirements
- Mask API keys: Show only first 3 + last 6 characters
- Mask emails: Show only first character + domain
- Never log full questions at INFO level (only at DEBUG, sanitized)
- Never log full API responses at INFO level (only at DEBUG, sanitized)
- All PII must be sanitized before logging

## Implementation Notes
- Use Python's standard logging module
- Consider using structured logging (JSON) for machine parsing
- Ensure log rotation if file logging enabled
- Handle file write errors gracefully (fallback to stderr only)

## Validation Checklist
- [ ] logging_config.py implements async logging
- [ ] utils.py implements all sanitization functions
- [ ] Server startup logged
- [ ] Query operations logged
- [ ] Errors logged with context
- [ ] Log levels configurable via env var
- [ ] Logs output to stderr
- [ ] Optional log file created
- [ ] No sensitive data in logs
- [ ] Sanitization functions tested
