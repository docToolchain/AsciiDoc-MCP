# AsciiDoc MCP Server Development Instructions

**ALWAYS follow these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.**

## Working Effectively

### Bootstrap, Build, and Test the Repository

The AsciiDoc MCP Server is a Python-based Model Context Protocol server that provides structured access to AsciiDoc documents. **NEVER CANCEL any builds or commands** - all operations complete quickly.

#### Prerequisites and Environment Setup
- **Requires Python 3.8+** (Python 3.12 is available and tested)
- **No additional SDK downloads required** - uses system Python and pip

#### Installation Process (Measured Times)
```bash
# Install the package in development mode
pip install -e .
# TIMING: ~16 seconds, NEVER CANCEL - Set timeout to 60+ seconds for safety
```

```bash
# Install development dependencies (for testing and linting)
pip install pytest pytest-asyncio black ruff
# TIMING: ~3 seconds, NEVER CANCEL - Set timeout to 30+ seconds for safety
# Note: The full dev dependencies via pip install -e ".[dev]" may timeout due to network issues
# Always install individual packages if the dev install fails
```

#### Testing and Validation
```bash
# Run full test suite
pytest -v
# TIMING: <1 second, NEVER CANCEL - Set timeout to 10+ seconds for safety
# Expected: 6 tests pass, covering document analysis, metadata extraction, includes, and search
```

```bash
# Test CLI functionality
asciidoc-mcp-server --version
# Expected output: 0.1.0
```

#### Code Quality and Linting
```bash
# Format code with Black
black src/
# TIMING: <1 second

# Check and fix linting issues with Ruff  
ruff check --fix src/
# TIMING: <1 second

# Check formatting
black --check src/
ruff check src/
# Note: Black will pass, Ruff may report some line length issues in docstrings and descriptions
# These are acceptable and don't affect functionality
```

### Manual Validation Scenarios

**CRITICAL**: Always manually validate functionality after making changes by running these scenarios:

#### Test Document Structure Analysis
```bash
python -c "
import asyncio
from src.asciidoc_mcp.asciidoc_processor import AsciiDocProcessor
import json

async def test():
    processor = AsciiDocProcessor()
    result = await processor.analyze_document_structure('demo.adoc')
    print(json.dumps(result, indent=2))
    assert result['title'] == 'Sample AsciiDoc Document'
    assert result['total_headings'] == 9
    print('✓ Document structure analysis works correctly')

asyncio.run(test())
"
```

#### Test Metadata Extraction
```bash
python -c "
import asyncio
from src.asciidoc_mcp.asciidoc_processor import AsciiDocProcessor
import json

async def test():
    processor = AsciiDocProcessor()
    result = await processor.extract_metadata('demo.adoc')
    print(json.dumps(result, indent=2))
    assert result['author'] == 'docToolchain Team'
    assert result['email'] == 'info@doctoolchain.org'
    print('✓ Metadata extraction works correctly')

asyncio.run(test())
"
```

#### Test Include Resolution
```bash
python -c "
import asyncio
from src.asciidoc_mcp.asciidoc_processor import AsciiDocProcessor
import json

async def test():
    processor = AsciiDocProcessor()
    result = await processor.find_includes('demo.adoc', recursive=False)
    print(json.dumps(result, indent=2))
    assert result['total_includes'] == 1
    assert 'ADR001-Idea.adoc' in result['includes'][0]['path']
    print('✓ Include resolution works correctly')

asyncio.run(test())
"
```

#### Test Content Search
```bash
python -c "
import asyncio
from src.asciidoc_mcp.asciidoc_processor import AsciiDocProcessor
import json

async def test():
    processor = AsciiDocProcessor()
    result = await processor.search_content('MCP server', 'demo.adoc')
    print(json.dumps(result, indent=2))
    assert result['total_matches'] == 6
    print('✓ Content search works correctly')

asyncio.run(test())
"
```

#### Test Server Startup
```bash
# The server starts correctly but will wait for MCP protocol input
# This test verifies the CLI entry point works
timeout 2 asciidoc-mcp-server || echo "✓ Server starts correctly (timeout expected)"
```

## Project Structure and Key Files

### Repository Layout
```
.
├── README.md                    # Project documentation  
├── pyproject.toml              # Python project configuration
├── demo.adoc                   # Sample AsciiDoc document for testing
├── src/
│   ├── asciidoc_mcp/
│   │   ├── __init__.py         # Package initialization
│   │   ├── cli.py              # Command-line interface entry point
│   │   ├── server.py           # MCP server implementation
│   │   └── asciidoc_processor.py # Core AsciiDoc processing logic
│   └── docs/
│       └── arc42/
│           └── adrs/
│               └── ADR001-Idea.adoc # Architecture decision record
└── tests/
    ├── __init__.py
    └── test_asciidoc_processor.py # Unit tests for processor functionality
```

### Key Components

- **`asciidoc_processor.py`** - Core logic for analyzing AsciiDoc documents, extracting metadata, resolving includes, and searching content
- **`server.py`** - MCP server implementation with tool registration and request handling  
- **`cli.py`** - Command-line entry point that starts the MCP server
- **`demo.adoc`** - Sample document that includes ADR001-Idea.adoc for testing include resolution

## MCP Server Tools

The server provides 4 main tools:

1. **`analyze_document_structure`** - Parse heading hierarchy and document structure
2. **`find_includes`** - Discover and resolve include directives recursively  
3. **`extract_metadata`** - Extract document attributes and file metadata
4. **`search_content`** - Search content with context (2 lines before/after matches)

## Installation and Usage as MCP Server

### Install via uvx (Recommended)
```bash
uvx --from git+https://github.com/docToolchain/AsciiDoc-MCP asciidoc-mcp-server
```

### MCP Client Configuration
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

### Combined with Serena MCP
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

## Development Workflow

### Making Changes
1. **Always validate your environment first**: Run `pip install -e .` and `pytest -v`
2. **Make your changes** to the appropriate files
3. **Run tests immediately**: `pytest -v` to ensure no regressions
4. **Format code**: `black src/` and `ruff check --fix src/`
5. **Manual validation**: Run the validation scenarios above to test functionality
6. **ALWAYS verify the CLI still works**: `asciidoc-mcp-server --version`

### Adding New Features
- Add tests in `tests/test_asciidoc_processor.py` following the existing pattern
- Implement functionality in `asciidoc_processor.py`
- Add MCP tool registration in `server.py` if exposing new functionality
- Update tool schemas and handlers following the existing patterns

### Common Issues and Solutions
- **Import errors**: Run `pip install -e .` to ensure package is properly installed
- **Test failures**: Check that all test AsciiDoc files exist and have expected content
- **Linting errors**: Run `black src/` then `ruff check --fix src/`  
- **MCP server not starting**: Verify `asciidoc-mcp-server --version` works first

## Critical Development Rules

- **NEVER CANCEL** any build or test commands - they complete in seconds
- **ALWAYS run manual validation scenarios** after making changes to ensure functionality works end-to-end
- **Format code** with Black and Ruff before committing changes
- **Test immediately** after making changes - tests run in <1 second
- **Use demo.adoc** for manual testing - it contains realistic AsciiDoc content with includes

## File Timing Reference

- `pip install -e .`: ~16 seconds  
- `pytest -v`: <1 second
- `black src/`: <1 second  
- `ruff check src/`: <1 second
- Manual validation scripts: <5 seconds each
- Server startup verification: <2 seconds

**All operations are fast - always wait for completion and never cancel prematurely.**