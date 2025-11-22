# Task 06 Implementation Plan: Mock Server and Testing Infrastructure

## 1. Issue
Implement a lightweight mock ICAET API server and pytest infrastructure to enable testing without real credentials. Currently `mock_server.py` and `conftest.py` contain only stubs with no functionality. Tests require a mock server that matches the real ICAET API contract and pytest fixtures to manage test lifecycle.

## 2. Solution
Create a Flask-based mock server in `mock_server.py` that mimics the ICAET API `/query` endpoint with validation and error scenarios. Implement pytest fixtures in `conftest.py` to manage mock server lifecycle (start/stop), provide test configuration (URLs, credentials), and configure httpx mocking for unit tests.

**Technical rationale:**
- Flask in test mode provides lightweight HTTP server for integration tests
- pytest-httpx enables unit tests without running actual server
- Random port selection prevents test conflicts
- Session-scoped fixtures minimize server startup overhead
- Function-scoped fixtures ensure test isolation
- Mock responses match real API contract from `tools.py`

## 3. Implementation Steps

### 3.1 Implement Flask Mock Server (mock_server.py)

1. **Import required modules:**
   - Import `flask` module (`Flask`, `request`, `jsonify`)
   - Import `typing` module (`Optional`)
   - Update module docstring to: "Mock ICAET server for testing."

2. **Create Flask application:**
   - Create function `create_app() -> Flask`
   - Initialize `app = Flask(__name__)`
   - Configure `app.config["TESTING"] = True`

3. **Implement /query POST endpoint:**
   - Create route function `query_endpoint()` with decorator `@app.route("/query", methods=["POST"])`
   - Extract API key from request headers: `api_key = request.headers.get("x-api-key")`
   - Validate API key presence: if not api_key, return `jsonify({"error": "Invalid API key"})` with status code 401
   - Handle missing/invalid JSON: wrap `request.get_json()` in try/except, return `jsonify({"error": "Invalid JSON"})` with status code 400 on exception
   - Validate request body has "question" field: if "question" not in data, return `jsonify({"error": "Missing required field: question"})` with status code 400
   - Validate request body has "email" field: if "email" not in data, return `jsonify({"error": "Missing required field: email"})` with status code 400

4. **Implement test response scenarios:**
   - Extract question: `question = data["question"]`
   - Simulate server error: if `question == "trigger_server_error"`, return `jsonify({"error": "Internal server error"})` with status code 500
   - Return successful response: return `jsonify({"answer": "This is a mock response to your question.", "sources": ["mock_source.txt"], "confidence": 0.95})` with status code 200

5. **Add application factory return:**
   - Return `app` from `create_app()` function

### 3.2 Implement Pytest Fixtures (conftest.py)

6. **Import required modules:**
   - Import `pytest`
   - Import `threading`
   - Import `time`
   - Import `socket`
   - From `tests.mock_server` import `create_app`
   - Update module docstring to: "Pytest configuration and fixtures."

7. **Implement port finder utility:**
   - Create function `_find_free_port() -> int`
   - Create socket: `s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)`
   - Bind to port 0: `s.bind(("", 0))`
   - Get assigned port: `port = s.getsockname()[1]`
   - Close socket: `s.close()`
   - Return `port`

8. **Implement mock_icaet_server fixture:**
   - Create fixture function `mock_icaet_server()` with decorator `@pytest.fixture(scope="session")`
   - Find free port: `port = _find_free_port()`
   - Create Flask app: `app = create_app()`
   - Create server thread: `server_thread = threading.Thread(target=lambda: app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False), daemon=True)`
   - Start thread: `server_thread.start()`
   - Wait for server: `time.sleep(0.5)` (allow server to start)
   - Yield server info: `yield {"host": "127.0.0.1", "port": port, "url": f"http://127.0.0.1:{port}"}`
   - Cleanup in teardown: no explicit cleanup needed (daemon thread)

9. **Implement mock_icaet_url fixture:**
   - Create fixture function `mock_icaet_url(mock_icaet_server)` with decorator `@pytest.fixture(scope="session")`
   - Return URL string: `return mock_icaet_server["url"]`

10. **Implement valid_credentials fixture:**
    - Create fixture function `valid_credentials()` with decorator `@pytest.fixture(scope="function")`
    - Return dict: `return {"api_key": "test-api-key-12345", "email": "test@example.com"}`

11. **Implement httpx_mock configuration fixture:**
    - Create fixture function `mock_httpx_client()` with decorator `@pytest.fixture(scope="function")`
    - Add docstring: "Fixture for configuring httpx mocking in unit tests. Use pytest-httpx's httpx_mock fixture directly in tests."
    - Yield None: `yield None`

### 3.3 Add Fixture Documentation

12. **Add module-level documentation:**
    - Add comment block at top of conftest.py after docstring:
```
# Fixture Usage:
# 
# Integration Tests (uses real HTTP calls to mock server):
#   def test_example(mock_icaet_url, valid_credentials):
#       response = httpx.post(f"{mock_icaet_url}/query", ...)
# 
# Unit Tests (mocks HTTP client, no server needed):
#   def test_example(httpx_mock, valid_credentials):
#       httpx_mock.add_response(json={"answer": "test"})
#       # Your test code here
#
# Fixtures:
# - mock_icaet_server: Session-scoped, starts Flask server on random port
# - mock_icaet_url: Session-scoped, provides base URL string
# - valid_credentials: Function-scoped, provides test API key and email
# - httpx_mock: Provided by pytest-httpx plugin for mocking HTTP requests
```

## 4. Verification

**Manual Testing:**
1. Run `pytest --collect-only` - should collect test files without errors
2. Start mock server manually via Python REPL:
   - `from tests.mock_server import create_app`
   - `app = create_app()`
   - `app.run(port=5001)`
3. Test POST /query with curl:
   - Valid request: `curl -X POST http://127.0.0.1:5001/query -H "x-api-key: test" -H "Content-Type: application/json" -d '{"email":"test@example.com","question":"test"}'` → expect 200 OK
   - Missing API key: `curl -X POST http://127.0.0.1:5001/query -H "Content-Type: application/json" -d '{"email":"test@example.com","question":"test"}'` → expect 401
   - Invalid JSON: `curl -X POST http://127.0.0.1:5001/query -H "x-api-key: test" -H "Content-Type: application/json" -d 'invalid'` → expect 400
   - Missing question: `curl -X POST http://127.0.0.1:5001/query -H "x-api-key: test" -H "Content-Type: application/json" -d '{"email":"test@example.com"}'` → expect 400
   - Server error: `curl -X POST http://127.0.0.1:5001/query -H "x-api-key: test" -H "Content-Type: application/json" -d '{"email":"test@example.com","question":"trigger_server_error"}'` → expect 500

**Key Requirements:**
- mock_server.py implements Flask app with create_app() factory
- POST /query endpoint validates x-api-key header
- Endpoint validates request body structure (email, question fields)
- Returns 200 OK with mock answer for valid requests
- Returns 401 for missing API key
- Returns 400 for invalid JSON or missing fields
- Returns 500 for "trigger_server_error" question
- conftest.py implements all required fixtures
- mock_icaet_server fixture starts server on random port
- mock_icaet_url fixture provides URL string
- valid_credentials fixture provides test credentials
- Fixtures properly scoped (session vs function)
- No real ICAET API calls during tests
- Fixture usage documented in conftest.py

---

## IMPLEMENTATION CHECKLIST

### Mock Server (mock_server.py)
- [ ] Import Flask, request, jsonify from flask
- [ ] Import Optional from typing
- [ ] Update module docstring to "Mock ICAET server for testing."
- [ ] Create function create_app() -> Flask
- [ ] Initialize app = Flask(__name__)
- [ ] Set app.config["TESTING"] = True
- [ ] Create @app.route("/query", methods=["POST"]) decorator
- [ ] Create query_endpoint() function
- [ ] Extract api_key from request.headers.get("x-api-key")
- [ ] Validate API key: if not api_key, return 401 with {"error": "Invalid API key"}
- [ ] Wrap request.get_json() in try/except for invalid JSON
- [ ] Return 400 with {"error": "Invalid JSON"} on JSON parse exception
- [ ] Validate "question" in data, return 400 with {"error": "Missing required field: question"} if missing
- [ ] Validate "email" in data, return 400 with {"error": "Missing required field: email"} if missing
- [ ] Extract question = data["question"]
- [ ] If question == "trigger_server_error", return 500 with {"error": "Internal server error"}
- [ ] Return 200 with {"answer": "This is a mock response to your question.", "sources": ["mock_source.txt"], "confidence": 0.95}
- [ ] Return app from create_app()

### Pytest Fixtures (conftest.py)
- [ ] Import pytest
- [ ] Import threading
- [ ] Import time
- [ ] Import socket
- [ ] Import create_app from tests.mock_server
- [ ] Update module docstring to "Pytest configuration and fixtures."
- [ ] Add fixture usage documentation comment block
- [ ] Create function _find_free_port() -> int
- [ ] Create socket, bind to port 0, get port, close socket, return port
- [ ] Create @pytest.fixture(scope="session") decorator for mock_icaet_server
- [ ] In mock_icaet_server: find free port
- [ ] In mock_icaet_server: create Flask app via create_app()
- [ ] In mock_icaet_server: create daemon thread running app.run()
- [ ] In mock_icaet_server: start thread
- [ ] In mock_icaet_server: sleep 0.5 seconds
- [ ] In mock_icaet_server: yield dict with host, port, url
- [ ] Create @pytest.fixture(scope="session") decorator for mock_icaet_url
- [ ] In mock_icaet_url: return mock_icaet_server["url"]
- [ ] Create @pytest.fixture(scope="function") decorator for valid_credentials
- [ ] In valid_credentials: return {"api_key": "test-api-key-12345", "email": "test@example.com"}
- [ ] Create @pytest.fixture(scope="function") decorator for mock_httpx_client
- [ ] In mock_httpx_client: add docstring about pytest-httpx usage
- [ ] In mock_httpx_client: yield None

### Verification
- [ ] Test: pytest --collect-only succeeds
- [ ] Test: Manual Flask server starts
- [ ] Test: Valid POST /query returns 200 OK with mock answer
- [ ] Test: Missing API key returns 401
- [ ] Test: Invalid JSON returns 400
- [ ] Test: Missing question field returns 400
- [ ] Test: Missing email field returns 400
- [ ] Test: trigger_server_error question returns 500
- [ ] Test: Fixtures are importable from conftest
- [ ] Test: mock_icaet_server fixture starts server
- [ ] Test: mock_icaet_url fixture returns URL string
- [ ] Test: valid_credentials fixture returns credentials dict
- [ ] Test: No errors in pytest collection

