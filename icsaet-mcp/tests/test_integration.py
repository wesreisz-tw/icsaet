"""Integration tests for the ICAET MCP server."""

import importlib
import sys

import httpx
import pytest


@pytest.mark.asyncio
async def test_integration_successful_query(mock_icaet_url, monkeypatch):
    # Arrange
    monkeypatch.setenv("ICAET_API_KEY", "test-api-key-12345")
    monkeypatch.setenv("USER_EMAIL", "test@example.com")
    if "icsaet_mcp.tools" in sys.modules:
        importlib.reload(sys.modules["icsaet_mcp.tools"])
    from icsaet_mcp.tools import query
    
    # Act
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{mock_icaet_url}/query",
            json={"question": "What is ICAET?", "email": "test@example.com"},
            headers={"x-api-key": "test-api-key-12345"}
        )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "sources" in data


@pytest.mark.asyncio
async def test_integration_unauthorized_no_api_key(mock_icaet_url, monkeypatch):
    # Arrange
    monkeypatch.setenv("ICAET_API_KEY", "")
    monkeypatch.setenv("USER_EMAIL", "test@example.com")
    
    # Act
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{mock_icaet_url}/query",
            json={"question": "test", "email": "test@example.com"},
            headers={}
        )
    
    # Assert
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_integration_missing_question_field(mock_icaet_url, monkeypatch):
    # Arrange
    monkeypatch.setenv("ICAET_API_KEY", "test-key")
    monkeypatch.setenv("USER_EMAIL", "test@example.com")
    
    # Act
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{mock_icaet_url}/query",
            json={"email": "test@example.com"},
            headers={"x-api-key": "test-key"}
        )
    
    # Assert
    assert response.status_code == 400
    assert "question" in response.json()["error"]


@pytest.mark.asyncio
async def test_integration_server_error_trigger(mock_icaet_url, monkeypatch):
    # Arrange
    monkeypatch.setenv("ICAET_API_KEY", "test-key")
    monkeypatch.setenv("USER_EMAIL", "test@example.com")
    
    # Act
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{mock_icaet_url}/query",
            json={"question": "trigger_server_error", "email": "test@example.com"},
            headers={"x-api-key": "test-key"}
        )
    
    # Assert
    assert response.status_code == 500


@pytest.mark.asyncio
async def test_integration_multi_query_sequence(mock_icaet_url, monkeypatch):
    # Arrange
    monkeypatch.setenv("ICAET_API_KEY", "test-key")
    monkeypatch.setenv("USER_EMAIL", "test@example.com")
    questions = ["Question 1", "Question 2", "Question 3"]
    
    # Act & Assert
    async with httpx.AsyncClient() as client:
        for question in questions:
            response = await client.post(
                f"{mock_icaet_url}/query",
                json={"question": question, "email": "test@example.com"},
                headers={"x-api-key": "test-key"}
            )
            assert response.status_code == 200
            assert "answer" in response.json()


@pytest.mark.asyncio
async def test_integration_mock_server_returns_sources(mock_icaet_url, monkeypatch):
    # Arrange
    monkeypatch.setenv("ICAET_API_KEY", "test-key")
    monkeypatch.setenv("USER_EMAIL", "test@example.com")
    
    # Act
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{mock_icaet_url}/query",
            json={"question": "test", "email": "test@example.com"},
            headers={"x-api-key": "test-key"}
        )
    
    # Assert
    data = response.json()
    assert "sources" in data
    assert "mock_source.txt" in data["sources"]


@pytest.mark.asyncio
async def test_integration_mock_server_returns_confidence(mock_icaet_url, monkeypatch):
    # Arrange
    monkeypatch.setenv("ICAET_API_KEY", "test-key")
    monkeypatch.setenv("USER_EMAIL", "test@example.com")
    
    # Act
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{mock_icaet_url}/query",
            json={"question": "test", "email": "test@example.com"},
            headers={"x-api-key": "test-key"}
        )
    
    # Assert
    data = response.json()
    assert "confidence" in data
    assert data["confidence"] == 0.95


@pytest.mark.asyncio
async def test_integration_uses_environment_email(mock_icaet_url, monkeypatch):
    # Arrange
    specific_email = "specific@example.com"
    monkeypatch.setenv("ICAET_API_KEY", "test-key")
    monkeypatch.setenv("USER_EMAIL", specific_email)
    
    # Act
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{mock_icaet_url}/query",
            json={"question": "test", "email": specific_email},
            headers={"x-api-key": "test-key"}
        )
    
    # Assert
    assert response.status_code == 200
