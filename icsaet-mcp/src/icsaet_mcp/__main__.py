"""Entry point for ICAET MCP server."""

import sys

from .server import mcp
from . import prompts
from . import tools  # Import tools to register the decorated functions


def main() -> None:
    """Run the MCP server."""
    try:
        mcp.run()
    except SystemExit:
        raise
    except Exception as e:
        sys.stderr.write(f"Error starting MCP server: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()

