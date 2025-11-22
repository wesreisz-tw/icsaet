"""Tests for MCP tools."""

import httpx
import pytest

from icsaet_mcp.tools import _query_impl


@pytest.mark.asyncio
async def test_query_successful_response(httpx_mock):
    # Arrange
    httpx_mock.add_response(
        method="POST",
        url="https://icaet-dev.wesleyreisz.com/query",
        json={"answer": "Test answer", "sources": ["source1.txt"], "confidence": 0.95},
        status_code=200
    )
    
    # Act
    result = await _query_impl("What is ICAET?", "test-api-key", "test@example.com")
    
    # Assert
    assert "answer" in result
    assert result["answer"] == "Test answer"
    assert "sources" in result
    assert "confidence" in result


@pytest.mark.asyncio
async def test_query_401_unauthorized(httpx_mock):
    # Arrange
    httpx_mock.add_response(
        method="POST",
        url="https://icaet-dev.wesleyreisz.com/query",
        status_code=401,
        text="Unauthorized"
    )
    
    # Act
    result = await _query_impl("test question", "test-api-key", "test@example.com")
    
    # Assert
    assert "error" in result
    assert "401" in result["error"]


@pytest.mark.asyncio
async def test_query_400_bad_request(httpx_mock):
    # Arrange
    httpx_mock.add_response(
        method="POST",
        url="https://icaet-dev.wesleyreisz.com/query",
        status_code=400,
        text="Bad Request"
    )
    
    # Act
    result = await _query_impl("test question", "test-api-key", "test@example.com")
    
    # Assert
    assert "error" in result
    assert "400" in result["error"]


@pytest.mark.asyncio
async def test_query_404_not_found(httpx_mock):
    # Arrange
    httpx_mock.add_response(
        method="POST",
        url="https://icaet-dev.wesleyreisz.com/query",
        status_code=404,
        text="Not Found"
    )
    
    # Act
    result = await _query_impl("test question", "test-api-key", "test@example.com")
    
    # Assert
    assert "error" in result
    assert "404" in result["error"]


@pytest.mark.asyncio
async def test_query_500_server_error(httpx_mock):
    # Arrange
    httpx_mock.add_response(
        method="POST",
        url="https://icaet-dev.wesleyreisz.com/query",
        status_code=500,
        text="Internal Server Error"
    )
    
    # Act
    result = await _query_impl("test question", "test-api-key", "test@example.com")
    
    # Assert
    assert "error" in result
    assert "500" in result["error"]


@pytest.mark.asyncio
async def test_query_timeout_error(httpx_mock):
    # Arrange
    httpx_mock.add_exception(httpx.TimeoutException("Request timeout"))
    
    # Act
    result = await _query_impl("test question", "test-api-key", "test@example.com")
    
    # Assert
    assert "error" in result
    assert "Request failed" in result["error"]


@pytest.mark.asyncio
async def test_query_connection_error(httpx_mock):
    # Arrange
    httpx_mock.add_exception(httpx.ConnectError("Connection failed"))
    
    # Act
    result = await _query_impl("test question", "test-api-key", "test@example.com")
    
    # Assert
    assert "error" in result
    assert "Request failed" in result["error"]


@pytest.mark.asyncio
async def test_query_invalid_json_response(httpx_mock):
    # Arrange
    httpx_mock.add_response(
        method="POST",
        url="https://icaet-dev.wesleyreisz.com/query",
        status_code=200,
        text="not valid json"
    )
    
    # Act
    result = await _query_impl("test question", "test-api-key", "test@example.com")
    
    # Assert
    assert "error" in result
    assert "Unexpected error" in result["error"]


@pytest.mark.asyncio
async def test_query_empty_question(httpx_mock):
    # Arrange
    httpx_mock.add_response(
        method="POST",
        url="https://icaet-dev.wesleyreisz.com/query",
        json={"answer": "Response to empty question", "sources": []},
        status_code=200
    )
    
    # Act
    result = await _query_impl("", "test-api-key", "test@example.com")
    
    # Assert
    assert "answer" in result


@pytest.mark.asyncio
async def test_query_long_question(httpx_mock):
    # Arrange
    long_question = "What is ICAET? " * 100
    httpx_mock.add_response(
        method="POST",
        url="https://icaet-dev.wesleyreisz.com/query",
        json={"answer": "Answer to long question", "sources": []},
        status_code=200
    )
    
    # Act
    result = await _query_impl(long_question, "test-api-key", "test@example.com")
    
    # Assert
    assert "answer" in result


@pytest.mark.asyncio
async def test_query_uses_correct_headers(httpx_mock):
    # Arrange
    httpx_mock.add_response(
        method="POST",
        url="https://icaet-dev.wesleyreisz.com/query",
        json={"answer": "Test", "sources": []},
        status_code=200
    )
    
    # Act
    await _query_impl("test", "test-api-key-12345", "test@example.com")
    
    # Assert
    request = httpx_mock.get_request()
    assert request.headers["x-api-key"] == "test-api-key-12345"
    assert request.headers["Content-Type"] == "application/json"


@pytest.mark.asyncio
async def test_query_uses_correct_endpoint(httpx_mock):
    # Arrange
    httpx_mock.add_response(
        method="POST",
        url="https://icaet-dev.wesleyreisz.com/query",
        json={"answer": "Test", "sources": []},
        status_code=200
    )
    
    # Act
    await _query_impl("test", "test-api-key", "test@example.com")
    
    # Assert
    request = httpx_mock.get_request()
    assert str(request.url) == "https://icaet-dev.wesleyreisz.com/query"
    assert request.method == "POST"
