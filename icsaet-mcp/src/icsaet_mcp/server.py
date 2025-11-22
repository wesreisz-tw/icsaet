"""MCP server implementation with environment variable validation."""

import os
import sys

from fastmcp import FastMCP

from .logging_config import setup_logging
from .utils import sanitize_api_key, sanitize_email

logger = setup_logging()

logger.info("Server starting")

ICAET_API_KEY = os.getenv("ICAET_API_KEY")
USER_EMAIL = os.getenv("USER_EMAIL")

if not ICAET_API_KEY:
    logger.error("Missing ICAET_API_KEY environment variable")
    sys.stderr.write("Error: ICAET_API_KEY environment variable is required\n")
    sys.exit(1)

if not USER_EMAIL:
    logger.error("Missing USER_EMAIL environment variable")
    sys.stderr.write("Error: USER_EMAIL environment variable is required\n")
    sys.exit(1)

logger.info(f"Configuration loaded [api_key={sanitize_api_key(ICAET_API_KEY)}, email={sanitize_email(USER_EMAIL)}]")

mcp = FastMCP("ICAET Query Server")

logger.info("Server ready")

