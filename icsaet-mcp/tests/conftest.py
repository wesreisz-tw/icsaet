"""Pytest configuration and fixtures."""

import pytest
import socket
import threading
import time

from tests.mock_server import create_app

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


def _find_free_port() -> int:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    port = s.getsockname()[1]
    s.close()
    return port


@pytest.fixture(scope="session")
def mock_icaet_server():
    port = _find_free_port()
    app = create_app()
    server_thread = threading.Thread(
        target=lambda: app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False),
        daemon=True
    )
    server_thread.start()
    time.sleep(0.5)
    yield {"host": "127.0.0.1", "port": port, "url": f"http://127.0.0.1:{port}"}


@pytest.fixture(scope="session")
def mock_icaet_url(mock_icaet_server):
    return mock_icaet_server["url"]


@pytest.fixture(scope="function")
def valid_credentials():
    return {"api_key": "test-api-key-12345", "email": "test@example.com"}


@pytest.fixture(scope="function")
def mock_httpx_client():
    """Fixture for configuring httpx mocking in unit tests. Use pytest-httpx's httpx_mock fixture directly in tests."""
    yield None

