"""
Web Content Extraction Toolset for LCP

Provides comprehensive tools for downloading, reading, and analyzing web content.
Supports HTML, text, PDF, and various other content types.
"""

from typing import Dict, List, Optional, Any, Union
import logging
import re
from pathlib import Path
import hashlib
from datetime import datetime

# Global state for lazy initialization
_session = None
_cache_dir = None
_initialized = False

logger = logging.getLogger(__name__)


def init_tools_library() -> Dict[str, Any]:
    """
    Initialize the web content extraction library.
    
    This function is called by LCP on first tool invocation.
    It performs lazy initialization of heavy dependencies.
    
    Returns:
        Dict with 'status' key indicating success or failure
    """
    global _session, _cache_dir, _initialized
    
    if _initialized:
        return {"status": "success", "message": "Already initialized"}
    
    try:
        import requests
        from bs4 import BeautifulSoup
        
        # Create session with reasonable defaults
        _session = requests.Session()
        _session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Create cache directory
        _cache_dir = Path(".lollms_code/cache/web_content")
        _cache_dir.mkdir(parents=True, exist_ok=True)
        
        _initialized = True
        logger.info("Web content extraction library initialized successfully")
        return {"status": "success", "message": "Web content extraction initialized"}
        
    except ImportError as e:
        error_msg = f"Failed to import required libraries: {e}. Install with: pip install requests beautifulsoup4 lxml"
        logger.error(error_msg)
        return {"status": "error", "error": error_msg}
    except Exception as e:
        error_msg = f"Failed to initialize web content extraction: {e}"
        logger.error(error_msg)
        return {"status": "error", "error": error_msg}


def _get_cache_path(url: str) -> Path:
    """Generate cache file path from URL."""
    url_hash = hashlib.md5(url.encode()).hexdigest()
    return _cache_dir / f"{url_hash}.cache"


def _fetch_url_content(url: str, timeout: int = 30) -> Dict[str, Any]:
    """
    Internal function to fetch URL content.
    
    Args:
        url: URL to fetch
        timeout: Request timeout in seconds
        
    Returns:
        Dictionary with content, headers, and metadata
    """
    global _session
    
    try:
        response = _session.get(url, timeout=timeout, allow_redirects=True)
        response.raise_for_status()
        
        content_type = response.headers.get('Content-Type', '').lower()
        
        return {
            "status": "success",
            "content": response.content,
            "text": response.text if 'text' in content_type or 'html' in content_type else None,
            "content_type": content_type,
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "url": response.url,  # Final URL after redirects
            "encoding": response.encoding
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


def _extract_text_from_html(html: str) -> str:
    """
    Extract readable text from HTML.
    
    Args:
        html: HTML content
        
    Returns:
        Extracted text
    """
    from bs4 import BeautifulSoup
    
    soup = BeautifulSoup(html, 'lxml')
    
    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()
    
    # Get text
    text = soup.get_text()
    
    # Break into lines and remove leading/trailing space
    lines = (line.strip() for line in text.splitlines())
    # Break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # Drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    
    return text


def fetch_url(url: str, extract_text: bool = True, timeout: int = 30) -> Dict[str, Any]:
    """
    Fetch content from a URL.
    
    Downloads the content and optionally extracts readable text from HTML.
    
    Args:
        url: URL to fetch
        extract_text: Whether to extract text from HTML (default: True)
        timeout: Request timeout in seconds (default: 30)
    
    Returns:
        Dictionary with 'content', 'content_type', 'metadata' keys.
        On error, returns dict with 'error' key.
    """
    global _initialized
    
    if not _initialized:
        init_result = init_tools_library()
        if init_result.get("status") == "error":
            return init_result
    
    try:
        result = _fetch_url_content(url, timeout)
        
        if result.get("status") == "error":
            return result
        
        content_type = result["content_type"]
        response_data = {
            "url": result["url"],
            "original_url": url,
            "content_type": content_type,
            "status_code": result["status_code"],
            "encoding": result["encoding"],
            "size_bytes": len(result["content"])
        }
        
        # Handle different content types
        if 'text/html' in content_type:
            response_data["html"] = result["text"]
            if extract_text:
                response_data["text"] = _extract_text_from_html(result["text"])
                response_data["text_length"] = len(response_data["text"])
        elif 'text/' in content_type or 'json' in content_type:
            response_data["text"] = result["text"]
            response_data["text_length"] = len(result["text"])
        elif 'application/pdf' in content_type:
            response_data["message"] = "PDF content detected. Use download_file to save and process PDF."
            response_data["binary"] = True
        else:
            response_data["message"] = f"Binary content type: {content_type}. Use download_file to save."
            response_data["binary"] = True
        
        return response_data
        
    except Exception as e:
        error_msg = f"Failed to fetch URL: {e}"
        logger.error(error_msg)
        return {"error": error_msg}


def read_content(url: str, max_chars: Optional[int] = None, 
                 start_line: int = 0, end_line: Optional[int] = None) -> Dict[str, Any]:
    """
    Read content from a URL with optional size limits.
    
    Args:
        url: URL to read
        max_chars: Maximum characters to return (None for all)
        start_line: Starting line number (0-indexed)
        end_line: Ending line number (None for all)
    
    Returns:
        Dictionary with 'content', 'total_lines', 'returned_lines' keys.
        On error, returns dict with 'error' key.
    """
    global _initialized
    
    if not _initialized:
        init_result = init_tools_library()
        if init_result.get("status") == "error":
            return init_result
    
    try:
        # Fetch content
        fetch_result = fetch_url(url, extract_text=True)
        
        if "error" in fetch_result:
            return fetch_result
        
        # Get text content
        text = fetch_result.get("text", "")
        
        if not text:
            return {"error": "No text content available"}
        
        # Split into lines
        lines = text.split('\n')
        total_lines = len(lines)
        
        # Apply line range
        if end_line is None:
            end_line = total_lines
        
        selected_lines = lines[start_line:end_line]
        content = '\n'.join(selected_lines)
        
        # Apply character limit
        truncated = False
        if max_chars and len(content) > max_chars:
            content = content[:max_chars]
            truncated = True
        
        return {
            "url": url,
            "content": content,
            "total_lines": total_lines,
            "returned_lines": len(selected_lines),
            "start_line": start_line,
            "end_line": end_line,
            "total_chars": len(text),
            "returned_chars": len(content),
            "truncated": truncated
        }
        
    except Exception as e:
        error_msg = f"Failed to read content: {e}"
        logger.error(error_msg)
        return {"error": error_msg}


def grep_content(url: str, pattern: str, case_sensitive: bool = False,
                 context_lines: int = 2, max_matches: int = 50) -> Dict[str, Any]:
    """
    Search for a pattern within URL content.
    
    Args:
        url: URL to search
        pattern: Regular expression pattern to search for
        case_sensitive: Whether search is case-sensitive (default: False)
        context_lines: Number of context lines to include (default: 2)
        max_matches: Maximum number of matches to return (default: 50)
    
    Returns:
        Dictionary with 'matches', 'total_matches' keys.
        Each match has 'line_number', 'line', 'context_before', 'context_after'.
        On error, returns dict with 'error' key.
    """
    global _initialized
    
    if not _initialized:
        init_result = init_tools_library()
        if init_result.get("status") == "error":
            return init_result
    
    try:
        # Fetch content
        fetch_result = fetch_url(url, extract_text=True)
        
        if "error" in fetch_result:
            return fetch_result
        
        text = fetch_result.get("text", "")
        
        if not text:
            return {"error": "No text content available"}
        
        # Compile regex
        flags = 0 if case_sensitive else re.IGNORECASE
        regex = re.compile(pattern, flags)
        
        # Search line by line
        lines = text.split('\n')
        matches = []
        
        for i, line in enumerate(lines):
            if regex.search(line):
                # Get context
                start = max(0, i - context_lines)
                end = min(len(lines), i + context_lines + 1)
                
                match_data = {
                    "line_number": i + 1,  # 1-indexed for display
                    "line": line,
                    "context_before": lines[start:i],
                    "context_after": lines[i+1:end]
                }
                
                matches.append(match_data)
                
                if len(matches) >= max_matches:
                    break
        
        return {
            "url": url,
            "pattern": pattern,
            "matches": matches,
            "total_matches": len(matches),
            "truncated": len(matches) >= max_matches
        }
        
    except re.error as e:
        error_msg = f"Invalid regex pattern: {e}"
        logger.error(error_msg)
        return {"error": error_msg}
    except Exception as e:
        error_msg = f"Failed to grep content: {e}"
        logger.error(error_msg)
        return {"error": error_msg}


def peek_content(url: str, position: str = "top", lines: int = 20) -> Dict[str, Any]:
    """
    Peek at the top or bottom of URL content.
    
    Args:
        url: URL to peek at
        position: "top" or "bottom" (default: "top")
        lines: Number of lines to show (default: 20)
    
    Returns:
        Dictionary with 'content', 'position', 'lines_shown' keys.
        On error, returns dict with 'error' key.
    """
    global _initialized
    
    if not _initialized:
        init_result = init_tools_library()
        if init_result.get("status") == "error":
            return init_result
    
    try:
        # Fetch content
        fetch_result = fetch_url(url, extract_text=True)
        
        if "error" in fetch_result:
            return fetch_result
        
        text = fetch_result.get("text", "")
        
        if not text:
            return {"error": "No text content available"}
        
        all_lines = text.split('\n')
        total_lines = len(all_lines)
        
        if position.lower() == "top":
            selected_lines = all_lines[:lines]
            start_line = 1
        elif position.lower() == "bottom":
            selected_lines = all_lines[-lines:]
            start_line = max(1, total_lines - lines + 1)
        else:
            return {"error": f"Invalid position: {position}. Use 'top' or 'bottom'."}
        
        content = '\n'.join(selected_lines)
        
        return {
            "url": url,
            "position": position,
            "content": content,
            "lines_shown": len(selected_lines),
            "total_lines": total_lines,
            "start_line": start_line,
            "end_line": start_line + len(selected_lines) - 1
        }
        
    except Exception as e:
        error_msg = f"Failed to peek content: {e}"
        logger.error(error_msg)
        return {"error": error_msg}


def extract_metadata(url: str) -> Dict[str, Any]:
    """
    Extract metadata from a web page.
    
    Extracts title, description, author, keywords, and other meta tags.
    
    Args:
        url: URL to extract metadata from
    
    Returns:
        Dictionary with metadata fields.
        On error, returns dict with 'error' key.
    """
    global _initialized
    
    if not _initialized:
        init_result = init_tools_library()
        if init_result.get("status") == "error":
            return init_result
    
    try:
        from bs4 import BeautifulSoup
        
        # Fetch content
        result = _fetch_url_content(url)
        
        if result.get("status") == "error":
            return {"error": result["error"]}
        
        html = result.get("text", "")
        
        if not html or 'html' not in result.get("content_type", ""):
            return {"error": "Not an HTML page"}
        
        soup = BeautifulSoup(html, 'lxml')
        
        metadata = {
            "url": result["url"],
            "title": None,
            "description": None,
            "author": None,
            "keywords": None,
            "og_title": None,
            "og_description": None,
            "og_image": None,
            "og_type": None,
            "twitter_card": None,
            "published_date": None,
            "modified_date": None
        }
        
        # Extract title
        title_tag = soup.find('title')
        if title_tag:
            metadata["title"] = title_tag.get_text().strip()
        
        # Extract meta tags
        for meta in soup.find_all('meta'):
            name = meta.get('name', '').lower()
            property_attr = meta.get('property', '').lower()
            content = meta.get('content', '')
            
            if name == 'description':
                metadata["description"] = content
            elif name == 'author':
                metadata["author"] = content
            elif name == 'keywords':
                metadata["keywords"] = content
            elif property_attr == 'og:title':
                metadata["og_title"] = content
            elif property_attr == 'og:description':
                metadata["og_description"] = content
            elif property_attr == 'og:image':
                metadata["og_image"] = content
            elif property_attr == 'og:type':
                metadata["og_type"] = content
            elif property_attr == 'twitter:card':
                metadata["twitter_card"] = content
            elif name == 'article:published_time':
                metadata["published_date"] = content
            elif name == 'article:modified_time':
                metadata["modified_date"] = content
        
        return metadata
        
    except Exception as e:
        error_msg = f"Failed to extract metadata: {e}"
        logger.error(error_msg)
        return {"error": error_msg}


def download_file(url: str, save_path: Optional[str] = None, 
                  chunk_size: int = 8192) -> Dict[str, Any]:
    """
    Download a file from a URL.
    
    Args:
        url: URL to download
        save_path: Path to save file (None for auto-generated in cache)
        chunk_size: Download chunk size in bytes (default: 8192)
    
    Returns:
        Dictionary with 'file_path', 'size_bytes', 'content_type' keys.
        On error, returns dict with 'error' key.
    """
    global _session, _cache_dir, _initialized
    
    if not _initialized:
        init_result = init_tools_library()
        if init_result.get("status") == "error":
            return init_result
    
    try:
        response = _session.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        # Determine save path
        if save_path is None:
            # Generate filename from URL
            filename = url.split('/')[-1].split('?')[0]
            if not filename:
                filename = f"download_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            save_path = _cache_dir / filename
        else:
            save_path = Path(save_path)
            save_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Download file
        total_size = 0
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    total_size += len(chunk)
        
        return {
            "url": url,
            "file_path": str(save_path),
            "size_bytes": total_size,
            "size_mb": round(total_size / (1024 * 1024), 2),
            "content_type": response.headers.get('Content-Type', 'unknown'),
            "status": "success"
        }
        
    except Exception as e:
        error_msg = f"Failed to download file: {e}"
        logger.error(error_msg)
        return {"error": error_msg}


# LCP Tool Discovery Metadata
__tools__ = [
    {
        "name": "fetch_url",
        "description": "Fetch content from a URL and extract readable text",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "URL to fetch"
                },
                "extract_text": {
                    "type": "boolean",
                    "description": "Extract readable text from HTML",
                    "default": True
                },
                "timeout": {
                    "type": "integer",
                    "description": "Request timeout in seconds",
                    "default": 30
                }
            },
            "required": ["url"]
        }
    },
    {
        "name": "read_content",
        "description": "Read content from a URL with optional size and line limits",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "URL to read"
                },
                "max_chars": {
                    "type": "integer",
                    "description": "Maximum characters to return (None for all)",
                    "default": None
                },
                "start_line": {
                    "type": "integer",
                    "description": "Starting line number (0-indexed)",
                    "default": 0
                },
                "end_line": {
                    "type": "integer",
                    "description": "Ending line number (None for all)",
                    "default": None
                }
            },
            "required": ["url"]
        }
    },
    {
        "name": "grep_content",
        "description": "Search for a pattern within URL content using regex",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "URL to search"
                },
                "pattern": {
                    "type": "string",
                    "description": "Regular expression pattern"
                },
                "case_sensitive": {
                    "type": "boolean",
                    "description": "Case-sensitive search",
                    "default": False
                },
                "context_lines": {
                    "type": "integer",
                    "description": "Number of context lines to include",
                    "default": 2
                },
                "max_matches": {
                    "type": "integer",
                    "description": "Maximum number of matches to return",
                    "default": 50
                }
            },
            "required": ["url", "pattern"]
        }
    },
    {
        "name": "peek_content",
        "description": "Peek at the top or bottom of URL content",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "URL to peek at"
                },
                "position": {
                    "type": "string",
                    "description": "Position to peek: 'top' or 'bottom'",
                    "default": "top",
                    "enum": ["top", "bottom"]
                },
                "lines": {
                    "type": "integer",
                    "description": "Number of lines to show",
                    "default": 20
                }
            },
            "required": ["url"]
        }
    },
    {
        "name": "extract_metadata",
        "description": "Extract metadata from a web page (title, description, author, etc.)",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "URL to extract metadata from"
                }
            },
            "required": ["url"]
        }
    },
    {
        "name": "download_file",
        "description": "Download a file from a URL to local storage",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "URL to download"
                },
                "save_path": {
                    "type": "string",
                    "description": "Path to save file (None for auto-generated)",
                    "default": None
                },
                "chunk_size": {
                    "type": "integer",
                    "description": "Download chunk size in bytes",
                    "default": 8192
                }
            },
            "required": ["url"]
        }
    }
]