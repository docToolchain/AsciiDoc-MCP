# Makefile for AsciiDoc MCP Server development

.PHONY: help install test lint format clean docker-build docker-run docs

help: ## Show this help message
	@echo "AsciiDoc MCP Server Development Commands"
	@echo "========================================"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install the package in development mode
	pip install -e ".[dev]"

test: ## Run the test suite
	pytest tests/ -v

lint: ## Run linting and formatting checks
	black src/
	ruff check src/

format: ## Format code using Black and Ruff
	black src/
	ruff check src/ --fix

type-check: ## Run type checking with mypy
	mypy src/

clean: ## Clean up build artifacts and cache files
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docker-build: ## Build Docker image
	docker build -t asciidoc-mcp .

docker-run: ## Run Docker container with current directory mounted
	docker run -i -v $(PWD):/workspace asciidoc-mcp

docker-dev: ## Run Docker container for development
	docker-compose up asciidoc-mcp

docs: ## Test documentation processing
	python -c "import asyncio; from asciidoc_mcp.asciidoc_processor import AsciiDocProcessor; asyncio.run(AsciiDocProcessor().analyze_document_structure('demo.adoc'))"

demo: ## Run demonstration of functionality
	python -c "import asyncio; exec(open('/tmp/test_functionality.py').read())" 2>/dev/null || python /tmp/test_functionality.py

version: ## Show version information
	asciidoc-mcp-server --version

serve: ## Start the MCP server
	asciidoc-mcp-server

all: lint test type-check ## Run all quality checks