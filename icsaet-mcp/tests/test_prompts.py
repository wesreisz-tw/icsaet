"""Tests for prompts."""

import pytest

from icsaet_mcp.prompts import _get_example_questions, _get_icaet_overview, _get_question_formatting


def test_icaet_overview_returns_string():
    # Arrange & Act
    result = _get_icaet_overview()
    
    # Assert
    assert isinstance(result, str)
    assert len(result) > 0


def test_icaet_overview_contains_key_sections():
    # Arrange & Act
    result = _get_icaet_overview()
    
    # Assert
    assert "What is ICAET?" in result
    assert "What information does it contain?" in result
    assert "Who would use this?" in result
    assert "How do I ask questions?" in result


def test_example_questions_returns_string():
    # Arrange & Act
    result = _get_example_questions()
    
    # Assert
    assert isinstance(result, str)
    assert len(result) > 0


def test_example_questions_contains_examples():
    # Arrange & Act
    result = _get_example_questions()
    
    # Assert
    assert "1." in result
    assert "2." in result
    assert "3." in result


def test_question_formatting_returns_string():
    # Arrange & Act
    result = _get_question_formatting()
    
    # Assert
    assert isinstance(result, str)
    assert len(result) > 0


def test_question_formatting_contains_best_practices():
    # Arrange & Act
    result = _get_question_formatting()
    
    # Assert
    assert "For Better Results" in result
    assert "What to Avoid" in result
