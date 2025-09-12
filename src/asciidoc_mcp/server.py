"""
MCP Server implementation for AsciiDoc document processing.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional, Sequence
import json
import sys

from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
from mcp import stdio_server
from mcp import types

from .asciidoc_processor import AsciiDocProcessor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("asciidoc-mcp")

# Create server instance
server = Server("asciidoc-mcp")

# Global processor instance
processor = AsciiDocProcessor()


@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    """List available tools for AsciiDoc processing."""
    return [
        types.Tool(
            name="analyze_document_structure",
            description="Parse and analyze the hierarchical structure of an AsciiDoc document",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the AsciiDoc file to analyze"
                    },
                    "include_content": {
                        "type": "boolean",
                        "description": "Whether to include the actual content of each section",
                        "default": False
                    }
                },
                "required": ["file_path"]
            }
        ),
        types.Tool(
            name="find_includes",
            description="Find and resolve include directives and their dependencies",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the AsciiDoc file to analyze for includes"
                    },
                    "recursive": {
                        "type": "boolean", 
                        "description": "Whether to recursively find includes in included files",
                        "default": True
                    }
                },
                "required": ["file_path"]
            }
        ),
        types.Tool(
            name="extract_metadata",
            description="Extract document attributes and metadata from AsciiDoc files",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the AsciiDoc file to extract metadata from"
                    }
                },
                "required": ["file_path"]
            }
        ),
        types.Tool(
            name="search_content",
            description="Search for content within AsciiDoc documents",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query string"
                    },
                    "file_path": {
                        "type": "string",
                        "description": "Path to the AsciiDoc file to search in (optional, searches all if not provided)"
                    },
                    "case_sensitive": {
                        "type": "boolean",
                        "description": "Whether the search should be case sensitive",
                        "default": False
                    }
                },
                "required": ["query"]
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: Optional[Dict[str, Any]]
) -> List[types.TextContent]:
    """Handle tool calls for AsciiDoc processing."""
    
    if not arguments:
        arguments = {}
    
    try:
        if name == "analyze_document_structure":
            file_path = arguments.get("file_path")
            include_content = arguments.get("include_content", False)
            
            if not file_path:
                raise ValueError("file_path is required")
            
            result = await processor.analyze_document_structure(file_path, include_content)
            return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
            
        elif name == "find_includes":
            file_path = arguments.get("file_path")
            recursive = arguments.get("recursive", True)
            
            if not file_path:
                raise ValueError("file_path is required")
            
            result = await processor.find_includes(file_path, recursive)
            return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
            
        elif name == "extract_metadata":
            file_path = arguments.get("file_path")
            
            if not file_path:
                raise ValueError("file_path is required")
            
            result = await processor.extract_metadata(file_path)
            return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
            
        elif name == "search_content":
            query = arguments.get("query")
            file_path = arguments.get("file_path")
            case_sensitive = arguments.get("case_sensitive", False)
            
            if not query:
                raise ValueError("query is required")
            
            result = await processor.search_content(query, file_path, case_sensitive)
            return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
            
        else:
            raise ValueError(f"Unknown tool: {name}")
            
    except Exception as e:
        logger.error(f"Error in tool {name}: {str(e)}")
        return [types.TextContent(
            type="text", 
            text=f"Error: {str(e)}"
        )]


async def main():
    """Main entry point for the MCP server."""
    # Run the server using stdio transport
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="asciidoc-mcp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                )
            )
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())