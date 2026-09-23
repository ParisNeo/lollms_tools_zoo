"""
DuckDuckGo Search Toolset for LCP

Provides free web search capabilities using DuckDuckGo API.
No API key required - completely free and privacy-focused.
"""

from typing import Dict, List, Optional, Any
import logging

# Global state for lazy initialization
_ddgs_instance = None
_initialized = False

logger = logging.getLogger(__name__)


def init_tools_library() -> Dict[str, Any]:
    """
    Initialize the DuckDuckGo search library.
    
    This function is called by LCP on first tool invocation.
    It performs lazy initialization of heavy dependencies.
    
    Returns:
        Dict with 'status' key indicating success or failure
    """
    global _ddgs_instance, _initialized
    
    if _initialized:
        return {"status": "success", "message": "Already initialized"}
    
    try:
        from duckduckgo_search import DDGS
        _ddgs_instance = DDGS()
        _initialized = True
        logger.info("DuckDuckGo search library initialized successfully")
        return {"status": "success", "message": "DuckDuckGo search initialized"}
    except ImportError as e:
        error_msg = f"Failed to import duckduckgo_search: {e}. Install with: pip install duckduckgo-search"
        logger.error(error_msg)
        return {"status": "error", "error": error_msg}
    except Exception as e:
        error_msg = f"Failed to initialize DuckDuckGo search: {e}"
        logger.error(error_msg)
        return {"status": "error", "error": error_msg}


def search_web(query: str, max_results: int = 10, region: str = "wt-wt") -> Dict[str, Any]:
    """
    Search the web using DuckDuckGo.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return (default: 10)
        region: Region code for localized results (default: "wt-wt" for worldwide)
    
    Returns:
        Dictionary with 'results' key containing list of search results.
        Each result has 'title', 'url', 'snippet' keys.
        On error, returns dict with 'error' key.
    """
    global _ddgs_instance, _initialized
    
    if not _initialized:
        init_result = init_tools_library()
        if init_result.get("status") == "error":
            return init_result
    
    try:
        results = []
        with _ddgs_instance as ddgs:
            for r in ddgs.text(query, region=region, max_results=max_results):
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("href", ""),
                    "snippet": r.get("body", "")
                })
        
        return {
            "results": results,
            "count": len(results),
            "query": query,
            "provider": "DuckDuckGo"
        }
    except Exception as e:
        error_msg = f"DuckDuckGo search failed: {e}"
        logger.error(error_msg)
        return {"error": error_msg}


def search_news(query: str, max_results: int = 10, region: str = "wt-wt") -> Dict[str, Any]:
    """
    Search for news articles using DuckDuckGo.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return (default: 10)
        region: Region code for localized results (default: "wt-wt")
    
    Returns:
        Dictionary with 'results' key containing list of news articles.
        Each result has 'title', 'url', 'snippet', 'date', 'source' keys.
        On error, returns dict with 'error' key.
    """
    global _ddgs_instance, _initialized
    
    if not _initialized:
        init_result = init_tools_library()
        if init_result.get("status") == "error":
            return init_result
    
    try:
        results = []
        with _ddgs_instance as ddgs:
            for r in ddgs.news(query, region=region, max_results=max_results):
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("url", ""),
                    "snippet": r.get("body", ""),
                    "date": r.get("date", ""),
                    "source": r.get("source", "")
                })
        
        return {
            "results": results,
            "count": len(results),
            "query": query,
            "provider": "DuckDuckGo News"
        }
    except Exception as e:
        error_msg = f"DuckDuckGo news search failed: {e}"
        logger.error(error_msg)
        return {"error": error_msg}


def search_images(query: str, max_results: int = 10, region: str = "wt-wt") -> Dict[str, Any]:
    """
    Search for images using DuckDuckGo.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return (default: 10)
        region: Region code for localized results (default: "wt-wt")
    
    Returns:
        Dictionary with 'results' key containing list of image results.
        Each result has 'title', 'url', 'thumbnail', 'source' keys.
        On error, returns dict with 'error' key.
    """
    global _ddgs_instance, _initialized
    
    if not _initialized:
        init_result = init_tools_library()
        if init_result.get("status") == "error":
            return init_result
    
    try:
        results = []
        with _ddgs_instance as ddgs:
            for r in ddgs.images(query, region=region, max_results=max_results):
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("image", ""),
                    "thumbnail": r.get("thumbnail", ""),
                    "source": r.get("source", "")
                })
        
        return {
            "results": results,
            "count": len(results),
            "query": query,
            "provider": "DuckDuckGo Images"
        }
    except Exception as e:
        error_msg = f"DuckDuckGo image search failed: {e}"
        logger.error(error_msg)
        return {"error": error_msg}


def search_videos(query: str, max_results: int = 10, region: str = "wt-wt") -> Dict[str, Any]:
    """
    Search for videos using DuckDuckGo.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return (default: 10)
        region: Region code for localized results (default: "wt-wt")
    
    Returns:
        Dictionary with 'results' key containing list of video results.
        Each result has 'title', 'url', 'duration', 'publisher' keys.
        On error, returns dict with 'error' key.
    """
    global _ddgs_instance, _initialized
    
    if not _initialized:
        init_result = init_tools_library()
        if init_result.get("status") == "error":
            return init_result
    
    try:
        results = []
        with _ddgs_instance as ddgs:
            for r in ddgs.videos(query, region=region, max_results=max_results):
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("content", ""),
                    "duration": r.get("duration", ""),
                    "publisher": r.get("publisher", "")
                })
        
        return {
            "results": results,
            "count": len(results),
            "query": query,
            "provider": "DuckDuckGo Videos"
        }
    except Exception as e:
        error_msg = f"DuckDuckGo video search failed: {e}"
        logger.error(error_msg)
        return {"error": error_msg}


# LCP Tool Discovery Metadata
__tools__ = [
    {
        "name": "search_web",
        "description": "Search the web using DuckDuckGo (free, no API key required)",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query string"
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of results to return",
                    "default": 10
                },
                "region": {
                    "type": "string",
                    "description": "Region code for localized results (e.g., 'us-en', 'uk-en', 'wt-wt' for worldwide)",
                    "default": "wt-wt"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "search_news",
        "description": "Search for news articles using DuckDuckGo",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query string"
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of results to return",
                    "default": 10
                },
                "region": {
                    "type": "string",
                    "description": "Region code for localized results",
                    "default": "wt-wt"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "search_images",
        "description": "Search for images using DuckDuckGo",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query string"
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of results to return",
                    "default": 10
                },
                "region": {
                    "type": "string",
                    "description": "Region code for localized results",
                    "default": "wt-wt"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "search_videos",
        "description": "Search for videos using DuckDuckGo",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query string"
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of results to return",
                    "default": 10
                },
                "region": {
                    "type": "string",
                    "description": "Region code for localized results",
                    "default": "wt-wt"
                }
            },
            "required": ["query"]
        }
    }
]