"""
Basic tests for AsciiDoc MCP server functionality.
"""

import pytest
import tempfile
import os
from pathlib import Path

from asciidoc_mcp.asciidoc_processor import AsciiDocProcessor


@pytest.fixture
def processor():
    """Create AsciiDocProcessor instance."""
    return AsciiDocProcessor()


@pytest.fixture
def sample_adoc_content():
    """Sample AsciiDoc content for testing."""
    return """= Main Document Title
:author: Test Author
:email: test@example.com
:revnumber: 1.0
:revdate: 2025-01-01

This is the main document introduction.

== Chapter 1: Getting Started

This is the first chapter content.

=== Section 1.1: Installation

Installation instructions here.

include::chapter2.adoc[]

== Chapter 3: Advanced Topics

Advanced content here.
"""


@pytest.fixture
def sample_include_content():
    """Sample included AsciiDoc content."""
    return """== Chapter 2: Configuration

This is chapter 2 content that gets included.

=== Section 2.1: Basic Config

Basic configuration details.
"""


@pytest.mark.asyncio
async def test_analyze_document_structure(processor, sample_adoc_content):
    """Test document structure analysis."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.adoc', delete=False) as f:
        f.write(sample_adoc_content)
        f.flush()
        
        try:
            result = await processor.analyze_document_structure(f.name)
            
            assert "error" not in result
            assert result["title"] == "Main Document Title"
            assert result["total_headings"] == 4  # Main title + Chapter 1 + Section 1.1 + Chapter 3
            assert len(result["structure"]) == 1  # One top-level heading
            
            # Check structure hierarchy
            main_heading = result["structure"][0]
            assert main_heading["title"] == "Main Document Title"
            assert main_heading["level"] == 1
            assert len(main_heading["children"]) == 2  # 2 direct children (Chapter 1 and Chapter 3)
            
            # Check that Chapter 1 has one subchild (Section 1.1)
            chapter1 = main_heading["children"][0]
            assert chapter1["title"] == "Chapter 1: Getting Started"
            assert len(chapter1["children"]) == 1
            assert chapter1["children"][0]["title"] == "Section 1.1: Installation"
            
        finally:
            os.unlink(f.name)


@pytest.mark.asyncio
async def test_extract_metadata(processor, sample_adoc_content):
    """Test metadata extraction."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.adoc', delete=False) as f:
        f.write(sample_adoc_content)
        f.flush()
        
        try:
            result = await processor.extract_metadata(f.name)
            
            assert "error" not in result
            assert result["title"] == "Main Document Title"
            assert result["author"] == "Test Author"
            assert result["email"] == "test@example.com"
            assert result["revision"] == "1.0"
            assert result["date"] == "2025-01-01"
            
            # Check attributes
            attributes = result["attributes"]
            assert attributes["author"] == "Test Author"
            assert attributes["email"] == "test@example.com"
            
        finally:
            os.unlink(f.name)


@pytest.mark.asyncio
async def test_find_includes(processor, sample_adoc_content):
    """Test include directive finding."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.adoc', delete=False) as f:
        f.write(sample_adoc_content)
        f.flush()
        
        try:
            result = await processor.find_includes(f.name, recursive=False)
            
            assert "error" not in result
            assert result["total_includes"] == 1
            assert len(result["includes"]) == 1
            
            include_info = result["includes"][0]
            assert include_info["path"] == "chapter2.adoc"
            assert include_info["depth"] == 0
            
        finally:
            os.unlink(f.name)


@pytest.mark.asyncio
async def test_search_content(processor, sample_adoc_content):
    """Test content search."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.adoc', delete=False) as f:
        f.write(sample_adoc_content)
        f.flush()
        
        try:
            result = await processor.search_content("Installation", f.name, case_sensitive=False)
            
            assert "error" not in result
            assert result["query"] == "Installation"
            assert result["total_matches"] == 2  # Section title and content
            
            # Check that we found matches
            assert len(result["results"]) == 2
            
        finally:
            os.unlink(f.name)


@pytest.mark.asyncio
async def test_nonexistent_file(processor):
    """Test handling of nonexistent files."""
    result = await processor.analyze_document_structure("/nonexistent/file.adoc")
    assert "error" in result
    assert "File not found" in result["error"]


def test_build_hierarchy(processor):
    """Test hierarchical structure building."""
    headings = [
        {"level": 1, "title": "Main", "line_number": 1, "position": 0},
        {"level": 2, "title": "Chapter 1", "line_number": 5, "position": 100},
        {"level": 3, "title": "Section 1.1", "line_number": 10, "position": 200},
        {"level": 2, "title": "Chapter 2", "line_number": 15, "position": 300},
    ]
    
    hierarchy = processor._build_hierarchy(headings)
    
    assert len(hierarchy) == 1  # One top-level
    main = hierarchy[0]
    assert main["title"] == "Main"
    assert len(main["children"]) == 2  # Two chapters
    
    chapter1 = main["children"][0]
    assert chapter1["title"] == "Chapter 1"
    assert len(chapter1["children"]) == 1  # One section
    
    section = chapter1["children"][0]
    assert section["title"] == "Section 1.1"
    assert len(section["children"]) == 0
    
    chapter2 = main["children"][1]
    assert chapter2["title"] == "Chapter 2"
    assert len(chapter2["children"]) == 0