"""Utility functions for the ICAET MCP server."""


def sanitize_api_key(key: str) -> str:
    """Sanitize API key by showing first 3 and last 6 characters."""
    try:
        if key is None:
            return "None"
        if not key:
            return ""
        if len(key) < 9:
            return "***"
        return f"{key[:3]}***{key[-6:]}"
    except Exception:
        return "***"


def sanitize_email(email: str) -> str:
    """Sanitize email by showing first character and domain."""
    try:
        if email is None:
            return "None"
        if not email:
            return ""
        parts = email.split('@')
        if len(parts) != 2:
            return "***"
        if not parts[0]:
            return "***@" + parts[1]
        return f"{parts[0][0]}***@{parts[1]}"
    except Exception:
        return "***"


def sanitize_question(question: str, max_len: int = 50) -> str:
    """Sanitize question by truncating to max length."""
    try:
        if question is None:
            return "None"
        if not question:
            return ""
        if len(question) > max_len:
            return question[:max_len] + "..."
        return question
    except Exception:
        return "***"

