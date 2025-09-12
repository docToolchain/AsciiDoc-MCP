# AsciiDoc MCP Server

A Model Context Protocol (MCP) server that provides structured access to AsciiDoc documents for Large Language Models (LLMs).

## Overview

This MCP server implements the architecture outlined in [ADR-001](src/docs/arc42/adrs/ADR001-Idea.adoc) for providing specialized AsciiDoc document analysis capabilities to LLMs. It enables AI assistants to understand document structure, resolve include dependencies, validate cross-references, and perform semantic analysis of AsciiDoc content.

## Features

The server provides the following tools:

### Core Document Analysis
- **`analyze_document_structure`** - Parse and analyze the hierarchical structure of AsciiDoc documents, including heading levels and section organization
- **`find_includes`** - Discover and resolve include directives and their dependencies recursively
- **`extract_metadata`** - Extract document attributes, author information, and file metadata
- **`search_content`** - Perform semantic search within AsciiDoc documents with context

### Planned Features (Future Releases)
- **`validate_cross_references`** - Validate internal cross-references and links
- **`analyze_assets`** - Analyze embedded images, diagrams, and other assets

## Installation

### From Source

1. Clone the repository:
```bash
git clone https://github.com/docToolchain/AsciiDoc-MCP.git
cd AsciiDoc-MCP
```

2. Install the package:
```bash
pip install -e .
```

### Using uvx (Recommended)

```bash
uvx --from git+https://github.com/docToolchain/AsciiDoc-MCP asciidoc-mcp-server
```

## Usage

### As an MCP Server

Configure your MCP client (like Claude Desktop) to use the AsciiDoc MCP server:

```json
{
  "mcpServers": {
    "asciidoc-mcp": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/docToolchain/AsciiDoc-MCP", "asciidoc-mcp-server"]
    }
  }
}
```

### Standalone Usage

You can also run the server directly:

```bash
asciidoc-mcp-server
```

### Combined with Serena MCP

This server is designed to work alongside [Serena MCP](https://github.com/oraios/serena) for comprehensive code and documentation analysis:

```json
{
  "mcpServers": {
    "serena": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/oraios/serena", "serena-mcp-server"]
    },
    "asciidoc-mcp": {
      "command": "uvx", 
      "args": ["--from", "git+https://github.com/docToolchain/AsciiDoc-MCP", "asciidoc-mcp-server"]
    }
  }
}
```

## Example Usage

### Analyze Document Structure

```python
# Tool: analyze_document_structure
{
  "file_path": "docs/manual.adoc",
  "include_content": true
}
```

Returns hierarchical structure of headings, sections, and optionally their content.

### Find Include Dependencies

```python
# Tool: find_includes
{
  "file_path": "main.adoc",
  "recursive": true
}
```

Returns all include directives and their resolved paths, useful for understanding document dependencies.

### Extract Metadata

```python
# Tool: extract_metadata
{
  "file_path": "document.adoc"
}
```

Returns document attributes, author information, revision details, and file metadata.

### Search Content

```python
# Tool: search_content
{
  "query": "architecture decision",
  "file_path": "docs/decisions.adoc",
  "case_sensitive": false
}
```

Searches for content with context, showing surrounding lines for better understanding.

## Development

### Requirements

- Python 3.8+
- MCP SDK
- AsciiDoc Python package

### Setup Development Environment

1. Clone and install in development mode:
```bash
git clone https://github.com/docToolchain/AsciiDoc-MCP.git
cd AsciiDoc-MCP
pip install -e ".[dev]"
```

2. Run tests:
```bash
pytest
```

3. Format code:
```bash
black src/
ruff check src/
```

### Architecture

The server consists of:

- **`server.py`** - Main MCP server implementation with tool registration and request handling
- **`asciidoc_processor.py`** - Core AsciiDoc processing logic and document analysis
- **`__init__.py`** - Package initialization and version information

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Ensure code formatting with Black and Ruff
6. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Related Projects

- [Serena MCP](https://github.com/oraios/serena) - Code intelligence MCP server
- [docToolchain](https://doctoolchain.org/) - Documentation toolchain
- [AsciiDoc](https://asciidoc.org/) - Text document format
- [Model Context Protocol](https://spec.modelcontextprotocol.io/) - Protocol specification