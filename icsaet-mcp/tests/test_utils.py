"""Tests for utility functions."""

import pytest

from icsaet_mcp.utils import sanitize_api_key, sanitize_email, sanitize_question


def test_sanitize_api_key_normal():
    # Arrange
    api_key = "abc123456789"
    
    # Act
    result = sanitize_api_key(api_key)
    
    # Assert
    assert result == "abc***456789"


def test_sanitize_api_key_short():
    # Arrange
    api_key = "short"
    
    # Act
    result = sanitize_api_key(api_key)
    
    # Assert
    assert result == "***"


def test_sanitize_api_key_empty():
    # Arrange
    api_key = ""
    
    # Act
    result = sanitize_api_key(api_key)
    
    # Assert
    assert result == ""


def test_sanitize_api_key_none():
    # Arrange
    api_key = None
    
    # Act
    result = sanitize_api_key(api_key)
    
    # Assert
    assert result == "None"


def test_sanitize_api_key_exactly_nine():
    # Arrange
    api_key = "123456789"
    
    # Act
    result = sanitize_api_key(api_key)
    
    # Assert
    assert result == "123***456789"


def test_sanitize_email_normal():
    # Arrange
    email = "user@example.com"
    
    # Act
    result = sanitize_email(email)
    
    # Assert
    assert result == "u***@example.com"


def test_sanitize_email_short_username():
    # Arrange
    email = "a@example.com"
    
    # Act
    result = sanitize_email(email)
    
    # Assert
    assert result == "a***@example.com"


def test_sanitize_email_invalid_no_at():
    # Arrange
    email = "notanemail"
    
    # Act
    result = sanitize_email(email)
    
    # Assert
    assert result == "***"


def test_sanitize_email_empty():
    # Arrange
    email = ""
    
    # Act
    result = sanitize_email(email)
    
    # Assert
    assert result == ""


def test_sanitize_email_none():
    # Arrange
    email = None
    
    # Act
    result = sanitize_email(email)
    
    # Assert
    assert result == "None"


def test_sanitize_email_multiple_at():
    # Arrange
    email = "user@@example.com"
    
    # Act
    result = sanitize_email(email)
    
    # Assert
    assert result == "***"


def test_sanitize_question_short():
    # Arrange
    question = "Hello?"
    
    # Act
    result = sanitize_question(question)
    
    # Assert
    assert result == "Hello?"


def test_sanitize_question_exactly_max():
    # Arrange
    question = "a" * 50
    
    # Act
    result = sanitize_question(question)
    
    # Assert
    assert result == "a" * 50


def test_sanitize_question_over_max():
    # Arrange
    question = "a" * 100
    
    # Act
    result = sanitize_question(question)
    
    # Assert
    assert result == "a" * 50 + "..."


def test_sanitize_question_empty():
    # Arrange
    question = ""
    
    # Act
    result = sanitize_question(question)
    
    # Assert
    assert result == ""


def test_sanitize_question_none():
    # Arrange
    question = None
    
    # Act
    result = sanitize_question(question)
    
    # Assert
    assert result == "None"


def test_sanitize_question_custom_max_len():
    # Arrange
    question = "Hello world"
    
    # Act
    result = sanitize_question(question, max_len=5)
    
    # Assert
    assert result == "Hello..."

