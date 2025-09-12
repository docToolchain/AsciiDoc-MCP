"""
AsciiDoc document processor for analyzing and extracting information from AsciiDoc files.
"""

import asyncio
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import logging

logger = logging.getLogger("asciidoc-mcp.processor")


class AsciiDocProcessor:
    """Processes AsciiDoc documents and extracts structured information."""
    
    def __init__(self):
        """Initialize the processor."""
        self.include_pattern = re.compile(r'^include::([^[\]]+)\[.*\]$', re.MULTILINE)
        self.heading_pattern = re.compile(r'^(=+)\s+(.+)$', re.MULTILINE)
        self.attribute_pattern = re.compile(r'^:([^:]+):\s*(.*)$', re.MULTILINE)
    
    async def analyze_document_structure(self, file_path: str, include_content: bool = False) -> Dict[str, Any]:
        """
        Analyze the hierarchical structure of an AsciiDoc document.
        
        Args:
            file_path: Path to the AsciiDoc file
            include_content: Whether to include the actual content of each section
            
        Returns:
            Dictionary containing the document structure
        """
        try:
            path = Path(file_path)
            if not path.exists():
                return {"error": f"File not found: {file_path}"}
            
            content = path.read_text(encoding='utf-8')
            
            # Extract headings and their levels
            headings = []
            for match in self.heading_pattern.finditer(content):
                level = len(match.group(1))  # Number of = characters
                title = match.group(2).strip()
                start_pos = match.start()
                
                heading_info = {
                    "level": level,
                    "title": title,
                    "line_number": content[:start_pos].count('\n') + 1,
                    "position": start_pos
                }
                
                if include_content:
                    # Extract content until next heading of same or higher level
                    content_start = match.end()
                    content_end = len(content)
                    
                    # Find next heading of same or higher level
                    for next_match in self.heading_pattern.finditer(content, content_start):
                        next_level = len(next_match.group(1))
                        if next_level <= level:
                            content_end = next_match.start()
                            break
                    
                    section_content = content[content_start:content_end].strip()
                    heading_info["content"] = section_content
                
                headings.append(heading_info)
            
            # Build hierarchical structure
            structure = self._build_hierarchy(headings)
            
            return {
                "file_path": file_path,
                "title": self._extract_document_title(content),
                "total_headings": len(headings),
                "structure": structure,
                "statistics": {
                    "lines": content.count('\n') + 1,
                    "characters": len(content),
                    "words": len(content.split())
                }
            }
            
        except Exception as e:
            logger.error(f"Error analyzing document structure: {e}")
            return {"error": str(e)}
    
    async def find_includes(self, file_path: str, recursive: bool = True) -> Dict[str, Any]:
        """
        Find and resolve include directives and their dependencies.
        
        Args:
            file_path: Path to the AsciiDoc file
            recursive: Whether to recursively find includes
            
        Returns:
            Dictionary containing include information
        """
        try:
            path = Path(file_path)
            if not path.exists():
                return {"error": f"File not found: {file_path}"}
            
            includes = []
            processed_files = set()
            
            def find_includes_in_file(current_path: Path, depth: int = 0) -> List[Dict[str, Any]]:
                if str(current_path) in processed_files:
                    return []  # Avoid circular includes
                
                processed_files.add(str(current_path))
                
                try:
                    content = current_path.read_text(encoding='utf-8')
                    file_includes = []
                    
                    for match in self.include_pattern.finditer(content):
                        include_path = match.group(1)
                        line_number = content[:match.start()].count('\n') + 1
                        
                        # Resolve relative path
                        if not Path(include_path).is_absolute():
                            resolved_path = (current_path.parent / include_path).resolve()
                        else:
                            resolved_path = Path(include_path)
                        
                        include_info = {
                            "path": include_path,
                            "resolved_path": str(resolved_path),
                            "exists": resolved_path.exists(),
                            "line_number": line_number,
                            "depth": depth,
                            "parent_file": str(current_path)
                        }
                        
                        # Add nested includes if recursive and file exists
                        if recursive and resolved_path.exists() and depth < 10:  # Prevent infinite recursion
                            nested_includes = find_includes_in_file(resolved_path, depth + 1)
                            include_info["nested_includes"] = nested_includes
                        
                        file_includes.append(include_info)
                    
                    return file_includes
                    
                except Exception as e:
                    logger.error(f"Error processing file {current_path}: {e}")
                    return []
            
            includes = find_includes_in_file(path)
            
            return {
                "file_path": file_path,
                "total_includes": len(includes),
                "includes": includes,
                "processed_files": list(processed_files)
            }
            
        except Exception as e:
            logger.error(f"Error finding includes: {e}")
            return {"error": str(e)}
    
    async def extract_metadata(self, file_path: str) -> Dict[str, Any]:
        """
        Extract document attributes and metadata from AsciiDoc files.
        
        Args:
            file_path: Path to the AsciiDoc file
            
        Returns:
            Dictionary containing metadata
        """
        try:
            path = Path(file_path)
            if not path.exists():
                return {"error": f"File not found: {file_path}"}
            
            content = path.read_text(encoding='utf-8')
            
            # Extract attributes
            attributes = {}
            for match in self.attribute_pattern.finditer(content):
                attr_name = match.group(1).strip()
                attr_value = match.group(2).strip()
                attributes[attr_name] = attr_value
            
            # Extract document title (first level 0 heading or title attribute)
            title = self._extract_document_title(content)
            
            # Extract author and revision info
            author = attributes.get('author', '')
            email = attributes.get('email', '')
            revision = attributes.get('revnumber', '')
            date = attributes.get('revdate', '')
            
            # File metadata
            stat = path.stat()
            
            return {
                "file_path": file_path,
                "title": title,
                "author": author,
                "email": email,
                "revision": revision,
                "date": date,
                "attributes": attributes,
                "file_info": {
                    "size_bytes": stat.st_size,
                    "modified": stat.st_mtime,
                    "created": stat.st_ctime
                }
            }
            
        except Exception as e:
            logger.error(f"Error extracting metadata: {e}")
            return {"error": str(e)}
    
    async def search_content(self, query: str, file_path: Optional[str] = None, case_sensitive: bool = False) -> Dict[str, Any]:
        """
        Search for content within AsciiDoc documents.
        
        Args:
            query: Search query string
            file_path: Optional path to specific file, searches current directory if not provided
            case_sensitive: Whether search should be case sensitive
            
        Returns:
            Dictionary containing search results
        """
        try:
            results = []
            files_searched = []
            
            if file_path:
                # Search in specific file
                path = Path(file_path)
                if not path.exists():
                    return {"error": f"File not found: {file_path}"}
                files_to_search = [path]
            else:
                # Search in all .adoc files in current directory and subdirectories
                files_to_search = list(Path.cwd().rglob("*.adoc"))
            
            flags = 0 if case_sensitive else re.IGNORECASE
            search_pattern = re.compile(re.escape(query), flags)
            
            for path in files_to_search:
                try:
                    content = path.read_text(encoding='utf-8')
                    files_searched.append(str(path))
                    
                    # Find all matches with context
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if search_pattern.search(line):
                            # Get context (2 lines before and after)
                            start_line = max(0, i - 2)
                            end_line = min(len(lines), i + 3)
                            context_lines = lines[start_line:end_line]
                            
                            result = {
                                "file": str(path),
                                "line_number": i + 1,
                                "line": line.strip(),
                                "context": context_lines,
                                "match_positions": [m.span() for m in search_pattern.finditer(line)]
                            }
                            results.append(result)
                    
                except Exception as e:
                    logger.error(f"Error searching file {path}: {e}")
                    continue
            
            return {
                "query": query,
                "case_sensitive": case_sensitive,
                "total_matches": len(results),
                "files_searched": files_searched,
                "results": results
            }
            
        except Exception as e:
            logger.error(f"Error searching content: {e}")
            return {"error": str(e)}
    
    def _extract_document_title(self, content: str) -> str:
        """Extract the document title from content."""
        # Look for level 0 heading (single =)
        title_match = re.search(r'^=\s+(.+)$', content, re.MULTILINE)
        if title_match:
            return title_match.group(1).strip()
        
        # Fall back to title attribute
        title_attr_match = re.search(r'^:title:\s*(.+)$', content, re.MULTILINE)
        if title_attr_match:
            return title_attr_match.group(1).strip()
        
        return ""
    
    def _build_hierarchy(self, headings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Build hierarchical structure from flat list of headings."""
        if not headings:
            return []
        
        hierarchy = []
        stack = []
        
        for heading in headings:
            level = heading["level"]
            
            # Pop from stack until we find appropriate parent level
            while stack and stack[-1]["level"] >= level:
                stack.pop()
            
            # Create heading with children array
            heading_with_children = heading.copy()
            heading_with_children["children"] = []
            
            if stack:
                # Add as child to parent
                stack[-1]["children"].append(heading_with_children)
            else:
                # Add to top level
                hierarchy.append(heading_with_children)
            
            # Add to stack for potential children
            stack.append(heading_with_children)
        
        return hierarchy