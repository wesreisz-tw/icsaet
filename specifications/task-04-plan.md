# Task 04 Implementation Plan: Logging System Implementation

## 1. Issue
Implement async structured logging with configurable levels, proper sanitization of sensitive data (API keys, emails, questions), and output to stderr and optional log files. Currently `logging_config.py` and `utils.py` are empty stubs with no functionality.

## 2. Solution
Create logging configuration in `logging_config.py` that sets up Python's standard logging module with async handlers, stderr output, configurable log levels via `ICAET_LOG_LEVEL` environment variable, and optional file output to `~/.icsaet-mcp/logs/server.log`. Implement sanitization functions in `utils.py` to mask sensitive data (API keys, emails, questions). Integrate logging throughout `server.py` and `tools.py` to capture server lifecycle events and query operations.

**Technical rationale:**
- Use Python's standard `logging` module with `StreamHandler` for stderr
- Use `RotatingFileHandler` for optional file logging (prevents disk space issues)
- Create log directory `~/.icsaet-mcp/logs/` with `pathlib.Path.mkdir(parents=True, exist_ok=True)`
- Use `logging.basicConfig()` or custom logger configuration for consistency
- Format: `%(asctime)s %(levelname)s %(message)s` (human-readable)
- Default log level: `INFO` if `ICAET_LOG_LEVEL` not set or invalid
- Valid levels: DEBUG, INFO, WARNING, ERROR
- Sanitization functions must never raise exceptions (use try/except with fallbacks)
- All logging statements use `logger.info()`, `logger.debug()`, `logger.error()` etc.
- Async logging: use `QueueHandler` + `QueueListener` for non-blocking I/O

## 3. Implementation Steps

### Step 1: Implement sanitization utilities in `utils.py`

1. **Import required modules:**
   - Import `re` for regex operations (email sanitization)

2. **Implement `sanitize_api_key(key: str) -> str` function:**
   - Add docstring: "Sanitize API key by showing first 3 and last 6 characters"
   - Handle None: `if key is None: return "None"`
   - Handle empty string: `if not key: return ""`
   - Handle short keys (< 9 chars): `if len(key) < 9: return "***"`
   - Normal case: `return f"{key[:3]}***{key[-6:]}"`
   - Wrap entire function in try/except returning "***" on any exception

3. **Implement `sanitize_email(email: str) -> str` function:**
   - Add docstring: "Sanitize email by showing first character and domain"
   - Handle None: `if email is None: return "None"`
   - Handle empty string: `if not email: return ""`
   - Split on '@': `parts = email.split('@')`
   - Handle invalid format (no @): `if len(parts) != 2: return "***"`
   - Return `f"{parts[0][0]}***@{parts[1]}"` (first char + *** + domain)
   - Handle empty username: check `if not parts[0]: return "***@" + parts[1]`
   - Wrap entire function in try/except returning "***" on any exception

4. **Implement `sanitize_question(question: str, max_len: int = 50) -> str` function:**
   - Add docstring: "Sanitize question by truncating to max length"
   - Handle None: `if question is None: return "None"`
   - Handle empty string: `if not question: return ""`
   - Truncate: `if len(question) > max_len: return question[:max_len] + "..."`
   - Otherwise: `return question`
   - Wrap entire function in try/except returning "***" on any exception

5. **Update module docstring:**
   - Change to: "Utility functions for the ICAET MCP server."
   - Remove `pass` statement

### Step 2: Implement logging configuration in `logging_config.py`

1. **Import required modules:**
   - Import `logging` from standard library
   - Import `logging.handlers` for `QueueHandler`, `QueueListener`, `RotatingFileHandler`
   - Import `queue` for `Queue`
   - Import `os` for environment variables
   - Import `sys` for stderr access
   - Import `pathlib.Path` for directory creation
   - Import `atexit` for cleanup registration

2. **Create `setup_logging()` function:**
   - Add docstring: "Configure async logging with stderr output and optional file logging"
   - Get log level from environment: `log_level_str = os.getenv("ICAET_LOG_LEVEL", "INFO").upper()`
   - Map to logging constant: `log_level = getattr(logging, log_level_str, logging.INFO)` (fallback to INFO if invalid)
   - Create log format: `log_format = "%(asctime)s %(levelname)s %(message)s"`
   - Create formatter: `formatter = logging.Formatter(log_format, datefmt="%Y-%m-%d %H:%M:%S")`

3. **Configure stderr handler in `setup_logging()`:**
   - Create stderr handler: `stderr_handler = logging.StreamHandler(sys.stderr)`
   - Set formatter: `stderr_handler.setFormatter(formatter)`
   - Set level: `stderr_handler.setLevel(log_level)`

4. **Configure optional file handler in `setup_logging()`:**
   - Create log directory: `log_dir = Path.home() / ".icsaet-mcp" / "logs"`
   - Create directory: `log_dir.mkdir(parents=True, exist_ok=True)`
   - Create file path: `log_file = log_dir / "server.log"`
   - Create rotating file handler: `file_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)` (10MB, 5 backups)
   - Set formatter: `file_handler.setFormatter(formatter)`
   - Set level: `file_handler.setLevel(log_level)`
   - Wrap file handler creation in try/except (if fails, log to stderr only)

5. **Configure async logging with queue in `setup_logging()`:**
   - Create queue: `log_queue = queue.Queue(-1)` (unlimited size)
   - Create queue handler: `queue_handler = QueueHandler(log_queue)`
   - Collect handlers: `handlers = [stderr_handler]` and append `file_handler` if successfully created
   - Create queue listener: `listener = QueueListener(log_queue, *handlers, respect_handler_level=True)`
   - Start listener: `listener.start()`
   - Register cleanup: `atexit.register(listener.stop)`

6. **Configure root logger in `setup_logging()`:**
   - Get root logger: `logger = logging.getLogger()`
   - Set level: `logger.setLevel(log_level)`
   - Add queue handler: `logger.addHandler(queue_handler)`
   - Return logger: `return logger`

7. **Create module-level logger:**
   - Add at module level: `logger = None` (will be initialized by setup_logging)
   - Update module docstring: "Logging configuration for the MCP server."
   - Remove `pass` statement

### Step 3: Integrate logging into `server.py`

1. **Import logging utilities:**
   - Import `from .logging_config import setup_logging`
   - Import `from .utils import sanitize_api_key, sanitize_email`

2. **Initialize logging before any other code:**
   - Add at top (after imports, before environment variable checks): `logger = setup_logging()`

3. **Add server startup log:**
   - Add after logger initialization: `logger.info("Server starting")`

4. **Update environment variable validation with logging:**
   - Before existing `if not ICAET_API_KEY:` check, add: `ICAET_API_KEY = os.getenv("ICAET_API_KEY")`
   - Change existing error to: `logger.error("Missing ICAET_API_KEY environment variable")`
   - Keep `sys.stderr.write()` for compatibility (or remove if logger.error is sufficient)
   - Do same for `USER_EMAIL` validation

5. **Add configuration loaded log:**
   - After successful validation, add: `logger.info(f"Configuration loaded [api_key={sanitize_api_key(ICAET_API_KEY)}, email={sanitize_email(USER_EMAIL)}]")`

6. **Add server ready log:**
   - After `mcp = FastMCP("ICAET Query Server")`, add: `logger.info("Server ready")`

### Step 4: Integrate logging into `tools.py`

1. **Import logging:**
   - Import `import logging` at top
   - Import `from .utils import sanitize_question` at top

2. **Get module logger:**
   - Add after imports: `logger = logging.getLogger(__name__)`

3. **Add query received log:**
   - At start of `query()` function (after docstring), add: `logger.info(f"Query received [question_length={len(question)}]")`

4. **Add debug log for full question:**
   - After INFO log, add: `logger.debug(f"Query question [question={sanitize_question(question, max_len=100)}]")`

5. **Add API success log:**
   - After `response.raise_for_status()`, before `return response.json()`, add: `logger.info(f"API request successful [status_code={response.status_code}]")`

6. **Add debug log for response:**
   - After success log, add: `logger.debug(f"API response [response_size={len(response.text)} bytes]")`

7. **Add error logging to exception handlers:**
   - In `httpx.HTTPStatusError` except block, add before return: `logger.error(f"API request failed [status_code={e.response.status_code}, error=HTTPStatusError]")`
   - In `httpx.RequestError` except block, add before return: `logger.error(f"API request failed [error=RequestError, message={str(e)}]")`
   - In general `Exception` except block, add before return: `logger.error(f"API request failed [error=UnexpectedException, message={str(e)}]")`

### Step 5: Install Package

1. **Install package in development mode:**
   - Run from workspace root: `cd /Users/wesleyreisz/work/mcp/icsaet/icsaet-mcp`
   - Execute: `/Users/wesleyreisz/.pyenv/versions/3.13.5/bin/python -m pip install -e .`
   - Verify installation: `python -m icsaet_mcp --help` should show FastMCP server banner
   - This makes the module importable system-wide without PYTHONPATH hacks

## 4. Verification

**Manual Testing:**
1. Test log levels:
   - Run without `ICAET_LOG_LEVEL` - should default to INFO
   - Run with `ICAET_LOG_LEVEL=DEBUG` - should show debug logs
   - Run with `ICAET_LOG_LEVEL=ERROR` - should only show errors
   - Run with `ICAET_LOG_LEVEL=invalid` - should default to INFO

2. Test sanitization:
   - API key logged as `sk-***abc123` format (first 3 + last 6)
   - Email logged as `u***@example.com` format (first char + domain)
   - Long questions truncated at INFO level
   - Full questions at DEBUG level (sanitized)

3. Test log output:
   - Logs appear on stderr (not stdout)
   - Log file created at `~/.icsaet-mcp/logs/server.log`
   - Log format matches: `2025-11-22 10:30:15 INFO Server starting`
   - Timestamps accurate to second

4. Test logging integration:
   - Server startup logs appear
   - Configuration loaded with sanitized credentials
   - Query received logs show question length
   - API success logs show status code
   - API errors logged with details
   - No PII in INFO/WARNING/ERROR logs

5. Test error handling:
   - Sanitization functions handle None gracefully
   - Sanitization functions handle empty strings
   - File logging failure doesn't crash server
   - Logs still work if file handler fails

**Key Requirements:**
- `logging_config.py` implements `setup_logging()` function
- `utils.py` implements all three sanitization functions
- Sanitization functions never raise exceptions
- API keys masked to first 3 + last 6 chars
- Emails masked to first char + domain
- Questions truncated to 50 chars at INFO level
- Log level configurable via `ICAET_LOG_LEVEL`
- Default log level is INFO
- Logs output to stderr
- Optional log file at `~/.icsaet-mcp/logs/server.log`
- Log rotation configured (10MB max, 5 backups)
- Async logging with queue (non-blocking)
- Server lifecycle logged (starting, config, ready)
- Query operations logged (received, success, errors)
- No sensitive data in INFO/WARNING/ERROR levels
- DEBUG level shows sanitized sensitive data
- Package installed with `pip install -e .` and importable via `python -m icsaet_mcp`

---

## IMPLEMENTATION CHECKLIST

### utils.py Implementation
- [ ] Import `re` module in `utils.py`
- [ ] Implement `sanitize_api_key(key: str) -> str` with None handling
- [ ] Implement `sanitize_api_key` with empty string handling
- [ ] Implement `sanitize_api_key` with short key handling (< 9 chars)
- [ ] Implement `sanitize_api_key` normal case (first 3 + *** + last 6)
- [ ] Wrap `sanitize_api_key` in try/except returning "***"
- [ ] Add docstring to `sanitize_api_key`
- [ ] Implement `sanitize_email(email: str) -> str` with None handling
- [ ] Implement `sanitize_email` with empty string handling
- [ ] Implement `sanitize_email` with @ split and validation
- [ ] Implement `sanitize_email` normal case (first char + *** + @ + domain)
- [ ] Wrap `sanitize_email` in try/except returning "***"
- [ ] Add docstring to `sanitize_email`
- [ ] Implement `sanitize_question(question: str, max_len: int = 50) -> str` with None handling
- [ ] Implement `sanitize_question` with empty string handling
- [ ] Implement `sanitize_question` truncation logic (max_len + "...")
- [ ] Wrap `sanitize_question` in try/except returning "***"
- [ ] Add docstring to `sanitize_question`
- [ ] Update module docstring in `utils.py`
- [ ] Remove `pass` statement from `utils.py`

### logging_config.py Implementation
- [ ] Import `logging` in `logging_config.py`
- [ ] Import `logging.handlers` (QueueHandler, QueueListener, RotatingFileHandler)
- [ ] Import `queue` module
- [ ] Import `os` module
- [ ] Import `sys` module
- [ ] Import `pathlib.Path`
- [ ] Import `atexit` module
- [ ] Create `setup_logging()` function with docstring
- [ ] Get `ICAET_LOG_LEVEL` from environment with default "INFO"
- [ ] Map log level string to logging constant with fallback
- [ ] Create log format string
- [ ] Create formatter with format and datefmt
- [ ] Create stderr StreamHandler
- [ ] Set formatter on stderr handler
- [ ] Set level on stderr handler
- [ ] Create log directory Path (`~/.icsaet-mcp/logs/`)
- [ ] Create directory with `mkdir(parents=True, exist_ok=True)`
- [ ] Create log file path (`server.log`)
- [ ] Wrap file handler creation in try/except
- [ ] Create RotatingFileHandler (10MB, 5 backups)
- [ ] Set formatter on file handler
- [ ] Set level on file handler
- [ ] Create Queue for async logging
- [ ] Create QueueHandler
- [ ] Collect handlers list (stderr + file if available)
- [ ] Create QueueListener with handlers
- [ ] Start QueueListener
- [ ] Register listener.stop with atexit
- [ ] Get root logger
- [ ] Set logger level
- [ ] Add queue handler to root logger
- [ ] Return logger from setup_logging
- [ ] Update module docstring in `logging_config.py`
- [ ] Remove `pass` statement from `logging_config.py`

### server.py Integration
- [ ] Import `setup_logging` from `.logging_config` in `server.py`
- [ ] Import `sanitize_api_key, sanitize_email` from `.utils` in `server.py`
- [ ] Call `logger = setup_logging()` at top of `server.py` (after imports)
- [ ] Add `logger.info("Server starting")` log
- [ ] Add `logger.error("Missing ICAET_API_KEY environment variable")` in validation
- [ ] Add `logger.error("Missing USER_EMAIL environment variable")` in validation
- [ ] Add configuration loaded log with sanitized credentials after validation
- [ ] Add `logger.info("Server ready")` after mcp creation

### tools.py Integration
- [ ] Import `logging` module in `tools.py`
- [ ] Import `sanitize_question` from `.utils` in `tools.py`
- [ ] Create module logger with `logging.getLogger(__name__)`
- [ ] Add `logger.info` for query received with question_length
- [ ] Add `logger.debug` for full question (sanitized, max_len=100)
- [ ] Add `logger.info` for API success with status_code
- [ ] Add `logger.debug` for API response size
- [ ] Add `logger.error` in HTTPStatusError handler with status_code
- [ ] Add `logger.error` in RequestError handler with error message
- [ ] Add `logger.error` in general Exception handler with error message

### Package Installation
- [ ] Navigate to package directory: `cd /Users/wesleyreisz/work/mcp/icsaet/icsaet-mcp`
- [ ] Install in editable mode: `pip install -e .`
- [ ] Verify module importable: `python -m icsaet_mcp --help`
- [ ] Confirm no ModuleNotFoundError when running server

### Verification Tests
- [ ] Test: Server starts with default INFO level
- [ ] Test: `ICAET_LOG_LEVEL=DEBUG` shows debug logs
- [ ] Test: `ICAET_LOG_LEVEL=ERROR` shows only errors
- [ ] Test: Invalid `ICAET_LOG_LEVEL` defaults to INFO
- [ ] Test: API key sanitized correctly (first 3 + last 6)
- [ ] Test: Email sanitized correctly (first char + domain)
- [ ] Test: Question truncated at INFO level
- [ ] Test: Full question shown at DEBUG level
- [ ] Test: Logs output to stderr
- [ ] Test: Log file created at `~/.icsaet-mcp/logs/server.log`
- [ ] Test: Log format matches specification
- [ ] Test: Server startup logged
- [ ] Test: Configuration loaded logged
- [ ] Test: Query received logged
- [ ] Test: API success logged
- [ ] Test: API errors logged
- [ ] Test: No PII in INFO logs
- [ ] Test: Sanitization handles None
- [ ] Test: Sanitization handles empty strings
- [ ] Test: File logging failure doesn't crash server
- [ ] Test: Package installed and importable without PYTHONPATH
- [ ] Test: `python -m icsaet_mcp` runs without ModuleNotFoundError

