# AsciiDoc-MCP Server

A specialized Model Context Protocol (MCP) server that provides structured AsciiDoc documentation support for Large Language Models (LLMs).

## Overview

This project implements a standalone MCP server designed to give LLMs intelligent access to AsciiDoc-based documentation structures, enabling enhanced documentation workflows and architectural decision support.

## Features

- **Document Structure Analysis**: Parse AsciiDoc heading hierarchies and document relationships
- **Include Resolution**: Resolve and analyze AsciiDoc include directives and dependencies
- **Cross-Reference Validation**: Validate internal cross-references within documentation
- **Content Search**: Semantic search capabilities within AsciiDoc content
- **Metadata Extraction**: Extract document attributes and configuration information
- **Asset Analysis**: Analyze embedded images, diagrams, and other assets

## Project Structure

```
.
├── dtcw                        # docToolchain wrapper script (Unix)
├── dtcw.bat                    # docToolchain wrapper script (Windows)
├── dtcw.ps1                    # docToolchain wrapper script (PowerShell)
├── docToolchainConfig.groovy   # docToolchain configuration
├── build.gradle                # Gradle build configuration
├── src/
│   └── docs/
│       ├── arc42/              # Architecture documentation (arc42 template)
│       │   ├── arc42.adoc      # Main architecture document
│       │   ├── src/            # Individual arc42 sections
│       │   └── adrs/           # Architecture Decision Records
│       └── images/             # Documentation images and diagrams
└── build/
    └── docs/                   # Generated documentation (HTML, PDF)
```

## Documentation

This project uses [docToolchain](https://doctoolchain.github.io/docToolchain/) for documentation generation and the [arc42](https://arc42.org/) template for architecture documentation.

### Prerequisites

- Java 17+ (automatically installed via dtcw)
- Docker (optional, for containerized builds)

### Building Documentation

#### Quick Start

```bash
# Generate HTML documentation
./dtcw generateHTML

# Generate PDF documentation  
./dtcw generatePDF

# Generate both formats
./dtcw generateSite
```

#### Using Docker (No Local Java Required)

```bash
# Generate HTML using Docker
./dtcw docker generateHTML

# Generate PDF using Docker
./dtcw docker generatePDF
```

#### First-time Setup

The docToolchain wrapper (`dtcw`) will automatically download and install the required dependencies:

```bash
# Install Java (if not using Docker)
./dtcw local install java

# Install docToolchain
./dtcw local install doctoolchain

# List available tasks
./dtcw tasks --group doctoolchain
```

### Generated Documentation

After running the build commands, you'll find:

- **HTML**: `build/docs/html5/arc42/arc42.html`
- **PDF**: `build/docs/pdf/arc42/arc42.pdf`

## Architecture Decision Records

This project maintains architectural decisions in the `src/docs/arc42/adrs/` directory:

- [ADR-001: Eigenständiger AsciiDoc-MCP-Server](src/docs/arc42/adrs/ADR001-Idea.adoc) - Decision to create a standalone AsciiDoc MCP server

## Development

### Configuration

The project is configured through:

- `docToolchainConfig.groovy` - Main docToolchain configuration
- `build.gradle` - Gradle build settings for documentation generation

### Key Configuration Points

```groovy
// docToolchainConfig.groovy
inputPath = 'src/docs'
outputPath = 'build/docs'
inputFiles = [
    [file: 'arc42/arc42.adoc', formats: ['html','pdf']],
]
```

### Available Tasks

```bash
# List all docToolchain tasks
./dtcw tasks --group doctoolchain

# Common tasks
./dtcw generateHTML      # Generate HTML documentation
./dtcw generatePDF       # Generate PDF documentation  
./dtcw generateSite      # Generate complete site
./dtcw exportEA          # Export Enterprise Architect diagrams
./dtcw exportChangeLog   # Export Git changelog
```

## Integration with MCP

This documentation structure is designed to support the future MCP server implementation, which will provide tools for:

1. **analyze_document_structure** - Parse heading hierarchy and document structure
2. **find_includes** - Resolve include directives and dependencies
3. **validate_cross_references** - Check internal cross-references
4. **search_content** - Semantic search in AsciiDoc content
5. **extract_metadata** - Document attributes and configuration
6. **analyze_assets** - Images, diagrams and other embedded assets

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Update documentation as needed
4. Generate and verify documentation builds successfully
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Documentation Guidelines

- Follow the arc42 template structure for architectural content
- Use AsciiDoc markup for all documentation
- Include architectural decision records (ADRs) for significant decisions
- Ensure all documentation builds successfully before committing
- Include diagrams and visual aids where helpful

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## References

- [Model Context Protocol Specification](https://spec.modelcontextprotocol.io/)
- [arc42 Architecture Template](https://arc42.org/)
- [docToolchain Documentation](https://doctoolchain.github.io/docToolchain/)
- [AsciiDoc Language Documentation](https://docs.asciidoctor.org/)

## Related Projects

- [Serena MCP Server](https://github.com/oraios/serena) - Code-focused MCP server for development workflows