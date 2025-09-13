#!/usr/bin/env python3
"""
Command line interface for AsciiDoc MCP Server.
"""

import asyncio
import logging
import sys

from . import __version__
from .server import main

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("asciidoc-mcp")


def cli_main():
    """CLI entry point."""
    if len(sys.argv) > 1 and sys.argv[1] == "--version":
        print(__version__)
        return

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    cli_main()
