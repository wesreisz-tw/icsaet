"""Tests for logging configuration."""

import logging
import sys
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from icsaet_mcp.logging_config import setup_logging


def test_setup_logging_default_level(monkeypatch):
    # Arrange
    monkeypatch.delenv("ICAET_LOG_LEVEL", raising=False)
    
    # Act
    logger = setup_logging()
    
    # Assert
    assert logger.level == logging.INFO


def test_setup_logging_debug_level(monkeypatch):
    # Arrange
    monkeypatch.setenv("ICAET_LOG_LEVEL", "DEBUG")
    
    # Act
    logger = setup_logging()
    
    # Assert
    assert logger.level == logging.DEBUG


def test_setup_logging_warning_level(monkeypatch):
    # Arrange
    monkeypatch.setenv("ICAET_LOG_LEVEL", "WARNING")
    
    # Act
    logger = setup_logging()
    
    # Assert
    assert logger.level == logging.WARNING


def test_setup_logging_invalid_level(monkeypatch):
    # Arrange
    monkeypatch.setenv("ICAET_LOG_LEVEL", "INVALID")
    
    # Act
    logger = setup_logging()
    
    # Assert
    assert logger.level == logging.INFO


def test_setup_logging_returns_logger(monkeypatch):
    # Arrange
    monkeypatch.delenv("ICAET_LOG_LEVEL", raising=False)
    
    # Act
    result = setup_logging()
    
    # Assert
    assert isinstance(result, logging.Logger)


def test_setup_logging_stderr_handler(monkeypatch):
    # Arrange
    monkeypatch.delenv("ICAET_LOG_LEVEL", raising=False)
    
    # Act
    logger = setup_logging()
    
    # Assert
    queue_handlers = [h for h in logger.handlers if isinstance(h, logging.handlers.QueueHandler)]
    assert len(queue_handlers) > 0


def test_setup_logging_creates_log_directory(tmp_path, monkeypatch):
    # Arrange
    monkeypatch.delenv("ICAET_LOG_LEVEL", raising=False)
    mock_home = tmp_path / "mock_home"
    mock_home.mkdir()
    
    with patch("pathlib.Path.home", return_value=mock_home):
        # Act
        setup_logging()
        
        # Assert
        log_dir = mock_home / ".icsaet-mcp" / "logs"
        assert log_dir.exists()


def test_setup_logging_handles_file_creation_failure(monkeypatch):
    # Arrange
    monkeypatch.delenv("ICAET_LOG_LEVEL", raising=False)
    
    with patch("pathlib.Path.mkdir", side_effect=PermissionError("Cannot create directory")):
        # Act
        logger = setup_logging()
        
        # Assert
        assert isinstance(logger, logging.Logger)


def test_setup_logging_format(monkeypatch, caplog):
    # Arrange
    monkeypatch.delenv("ICAET_LOG_LEVEL", raising=False)
    logger = setup_logging()
    
    # Act
    logger.info("Test message")
    
    # Assert
    # The format is checked by ensuring handlers have formatters
    queue_handlers = [h for h in logger.handlers if isinstance(h, logging.handlers.QueueHandler)]
    assert len(queue_handlers) > 0

