# AsciiDoc MCP Server Dockerfile
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y \
    git \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && update-ca-certificates

# Copy project files
COPY pyproject.toml README.md ./
COPY src/ ./src/

# Install the package with trusted hosts to handle SSL issues
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -e .

# Create workspace directory for mounted documentation
WORKDIR /workspace

# Set the entry point to the MCP server
ENTRYPOINT ["asciidoc-mcp-server"]

# Metadata
LABEL org.opencontainers.image.title="AsciiDoc MCP Server"
LABEL org.opencontainers.image.description="Model Context Protocol server for AsciiDoc document analysis"
LABEL org.opencontainers.image.vendor="docToolchain"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.source="https://github.com/docToolchain/AsciiDoc-MCP"