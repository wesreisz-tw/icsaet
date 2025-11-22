"""Tests for MCP server functionality."""

import os
import subprocess
import sys

import pytest
from fastmcp import FastMCP


def test_server_initialization_success(monkeypatch, tmp_path):
    # Arrange
    monkeypatch.setenv("ICAET_API_KEY", "test-api-key")
    monkeypatch.setenv("USER_EMAIL", "test@example.com")
    test_script = tmp_path / "test_import.py"
    test_script.write_text("""
import sys
sys.path.insert(0, '/Users/wesleyreisz/work/mcp/icsaet/icsaet-mcp/src')
from icsaet_mcp import server
print("SUCCESS")
""")
    
    # Act
    result = subprocess.run(
        [sys.executable, str(test_script)],
        capture_output=True,
        text=True,
        env={**os.environ, "ICAET_API_KEY": "test-api-key", "USER_EMAIL": "test@example.com"}
    )
    
    # Assert
    assert result.returncode == 0
    assert "SUCCESS" in result.stdout


def test_server_missing_icaet_api_key(tmp_path):
    # Arrange
    test_script = tmp_path / "test_import.py"
    test_script.write_text("""
import sys
sys.path.insert(0, '/Users/wesleyreisz/work/mcp/icsaet/icsaet-mcp/src')
from icsaet_mcp import server
""")
    env = {k: v for k, v in os.environ.items() if k != "ICAET_API_KEY"}
    env["USER_EMAIL"] = "test@example.com"
    
    # Act
    result = subprocess.run(
        [sys.executable, str(test_script)],
        capture_output=True,
        text=True,
        env=env
    )
    
    # Assert
    assert result.returncode == 1
    assert "ICAET_API_KEY" in result.stderr


def test_server_missing_user_email(tmp_path):
    # Arrange
    test_script = tmp_path / "test_import.py"
    test_script.write_text("""
import sys
sys.path.insert(0, '/Users/wesleyreisz/work/mcp/icsaet/icsaet-mcp/src')
from icsaet_mcp import server
""")
    env = {k: v for k, v in os.environ.items() if k != "USER_EMAIL"}
    env["ICAET_API_KEY"] = "test-api-key"
    
    # Act
    result = subprocess.run(
        [sys.executable, str(test_script)],
        capture_output=True,
        text=True,
        env=env
    )
    
    # Assert
    assert result.returncode == 1
    assert "USER_EMAIL" in result.stderr


def test_server_missing_both_credentials(tmp_path):
    # Arrange
    test_script = tmp_path / "test_import.py"
    test_script.write_text("""
import sys
sys.path.insert(0, '/Users/wesleyreisz/work/mcp/icsaet/icsaet-mcp/src')
from icsaet_mcp import server
""")
    env = {k: v for k, v in os.environ.items() if k not in ("ICAET_API_KEY", "USER_EMAIL")}
    
    # Act
    result = subprocess.run(
        [sys.executable, str(test_script)],
        capture_output=True,
        text=True,
        env=env
    )
    
    # Assert
    assert result.returncode == 1


def test_server_empty_api_key(tmp_path):
    # Arrange
    test_script = tmp_path / "test_import.py"
    test_script.write_text("""
import sys
sys.path.insert(0, '/Users/wesleyreisz/work/mcp/icsaet/icsaet-mcp/src')
from icsaet_mcp import server
""")
    
    # Act
    result = subprocess.run(
        [sys.executable, str(test_script)],
        capture_output=True,
        text=True,
        env={**os.environ, "ICAET_API_KEY": "", "USER_EMAIL": "test@example.com"}
    )
    
    # Assert
    assert result.returncode == 1


def test_server_empty_email(tmp_path):
    # Arrange
    test_script = tmp_path / "test_import.py"
    test_script.write_text("""
import sys
sys.path.insert(0, '/Users/wesleyreisz/work/mcp/icsaet/icsaet-mcp/src')
from icsaet_mcp import server
""")
    
    # Act
    result = subprocess.run(
        [sys.executable, str(test_script)],
        capture_output=True,
        text=True,
        env={**os.environ, "ICAET_API_KEY": "test-key", "USER_EMAIL": ""}
    )
    
    # Assert
    assert result.returncode == 1


def test_server_stderr_output_missing_api_key(tmp_path):
    # Arrange
    test_script = tmp_path / "test_import.py"
    test_script.write_text("""
import sys
sys.path.insert(0, '/Users/wesleyreisz/work/mcp/icsaet/icsaet-mcp/src')
from icsaet_mcp import server
""")
    env = {k: v for k, v in os.environ.items() if k != "ICAET_API_KEY"}
    env["USER_EMAIL"] = "test@example.com"
    
    # Act
    result = subprocess.run(
        [sys.executable, str(test_script)],
        capture_output=True,
        text=True,
        env=env
    )
    
    # Assert
    assert "ICAET_API_KEY environment variable is required" in result.stderr


def test_server_stderr_output_missing_email(tmp_path):
    # Arrange
    test_script = tmp_path / "test_import.py"
    test_script.write_text("""
import sys
sys.path.insert(0, '/Users/wesleyreisz/work/mcp/icsaet/icsaet-mcp/src')
from icsaet_mcp import server
""")
    env = {k: v for k, v in os.environ.items() if k != "USER_EMAIL"}
    env["ICAET_API_KEY"] = "test-key"
    
    # Act
    result = subprocess.run(
        [sys.executable, str(test_script)],
        capture_output=True,
        text=True,
        env=env
    )
    
    # Assert
    assert "USER_EMAIL environment variable is required" in result.stderr


def test_server_creates_mcp_instance(monkeypatch, tmp_path):
    # Arrange
    monkeypatch.setenv("ICAET_API_KEY", "test-key")
    monkeypatch.setenv("USER_EMAIL", "test@example.com")
    test_script = tmp_path / "test_import.py"
    test_script.write_text("""
import sys
sys.path.insert(0, '/Users/wesleyreisz/work/mcp/icsaet/icsaet-mcp/src')
from icsaet_mcp import server
from fastmcp import FastMCP
print("IS_FASTMCP:", isinstance(server.mcp, FastMCP))
""")
    
    # Act
    result = subprocess.run(
        [sys.executable, str(test_script)],
        capture_output=True,
        text=True,
        env={**os.environ, "ICAET_API_KEY": "test-key", "USER_EMAIL": "test@example.com"}
    )
    
    # Assert
    assert "IS_FASTMCP: True" in result.stdout


def test_server_mcp_has_correct_name(monkeypatch, tmp_path):
    # Arrange
    monkeypatch.setenv("ICAET_API_KEY", "test-key")
    monkeypatch.setenv("USER_EMAIL", "test@example.com")
    test_script = tmp_path / "test_import.py"
    test_script.write_text("""
import sys
sys.path.insert(0, '/Users/wesleyreisz/work/mcp/icsaet/icsaet-mcp/src')
from icsaet_mcp import server
print("NAME:", server.mcp.name)
""")
    
    # Act
    result = subprocess.run(
        [sys.executable, str(test_script)],
        capture_output=True,
        text=True,
        env={**os.environ, "ICAET_API_KEY": "test-key", "USER_EMAIL": "test@example.com"}
    )
    
    # Assert
    assert "ICAET Query Server" in result.stdout
