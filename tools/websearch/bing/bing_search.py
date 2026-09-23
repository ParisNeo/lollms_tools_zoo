"""
Bing Search Toolset for LCP

Provides web search capabilities using Microsoft Bing Search API.
Requires API key from Azure (free tier available: 1000 transactions/month).
"""

from typing import Dict, List, Optional, Any
import os
import logging

# Global state for lazy initialization
_subscription_key = None
_initialized = False

logger = logging.getLogger(__name__)


def init_tools_library() -> Dict[str, Any]:
    """
    Initialize the Bing search library.
    
    This function is called by LCP on first tool invocation.
    It loads the API key from environment variables.
    
    Returns:
        Dict with 'status' key indicating success or failure
    """
    global _subscription_key, _initialized
    
    if _initialized:
        return {"status": "success", "message": "Already initialized"}
    
    try:
        _subscription_key = os.getenv("BING_SEARCH_API_KEY")
        
        if not _subscription_key:
            error_msg = "BING_SEARCH_API_KEY not found in environment variables. Get a free key at: https://www.microsoft.com/en-us/bing/apis/bing-web-search-api"
            logger.error(error_msg)
            return {"status": "error", "error": error_msg}
        
        # Test import
        import requests
        
        _initialized = True
        logger.info("Bing search library initialized successfully")
        return {"status": "success", "message": "Bing search initialized"}
    except ImportError as e:
        error_msg = f"Failed to import requests: {e}. Install with: pip install requests"
        logger.error(error_msg)
        return {"status": "error", "error": error_msg}
    except Exception as e:
        error_msg = f"Failed to initialize Bing search: {e}"
        logger.error(error_msg)
        return {"status": "error", "error": error_msg}


def search_web(query: str, max_results: int = 10, market: str = "en-US") -> Dict[str, Any]:
    """
    Search the web using Bing Search API.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return (default: 10, max: 50)
        market: Market code for localized results (default: "en-US")
    
    Returns:
        Dictionary with 'results' key containing list of search results.
        Each result has 'title', 'url', 'snippet' keys.
        On error, returns dict with 'error' key.
    """
    global _subscription_key, _initialized
    
    if not _initialized:
        init_result = init_tools_library()
        if init_result.get("status") == "error":
            return init_result
    
    try:
        import requests
        
        endpoint = "https://api.bing.microsoft.com/v7.0/search"
        headers = {"Ocp-Apim-Subscription-Key": _subscription_key}
        params = {
            "q": query,
            "count": min(max_results, 50),
            "mkt": market,
            "responseFilter": "Webpages"
        }
        
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        results = []
        
        if "webPages" in data and "value" in data["webPages"]:
            for item in data["webPages"]["value"]:
                results.append({
                    "title": item.get("name", ""),
                    "url": item.get("url", ""),
                    "snippet": item.get("snippet", "")
                })
        
        return {
            "results": results,
            "count": len(results),
            "query": query,
            "provider": "Bing"
        }
    except Exception as e:
        error_msg = f"Bing search failed: {e}"
        logger.error(error_msg)
        return {"error": error_msg}


def search_news(query: str, max_results: int = 10, market: str = "en-US") -> Dict[str, Any]:
    """
    Search for news articles using Bing News Search API.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return (default: 10, max: 100)
        market: Market code for localized results (default: "en-US")
    
    Returns:
        Dictionary with 'results' key containing list of news articles.
        Each result has 'title', 'url', 'snippet', 'date', 'source' keys.
        On error, returns dict with 'error' key.
    """
    global _subscription_key, _initialized
    
    if not _initialized:
        init_result = init_tools_library()
        if init_result.get("status") == "error":
            return init_result
    
    try:
        import requests
        
        endpoint = "https://api.bing.microsoft.com/v7.0/news/search"
        headers = {"Ocp-Apim-Subscription-Key": _subscription_key}
        params = {
            "q": query,
            "count": min(max_results, 100),
            "mkt": market
        }
        
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        results = []
        
        if "value" in data:
            for item in data["value"]:
                results.append({
                    "title": item.get("name", ""),
                    "url": item.get("url", ""),
                    "snippet": item.get("description", ""),
                    "date": item.get("datePublished", ""),
                    "source": item.get("provider", [{}])[0].get("name", "")
                })
        
        return {
            "results": results,
            "count": len(results),
            "query": query,
            "provider": "Bing News"
        }
    except Exception as e:
        error_msg = f"Bing news search failed: {e}"
        logger.error(error_msg)
        return {"error": error_msg}


def search_images(query: str, max_results: int = 10, market: str = "en-US") -> Dict[str, Any]:
    """
    Search for images using Bing Image Search API.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return (default: 10, max: 150)
        market: Market code for localized results (default: "en-US")
    
    Returns:
        Dictionary with 'results' key containing list of image results.
        Each result has 'title', 'url', 'thumbnail', 'source' keys.
        On error, returns dict with 'error' key.
    """
    global _subscription_key, _initialized
    
    if not _initialized:
        init_result = init_tools_library()
        if init_result.get("status") == "error":
            return init_result
    
    try:
        import requests
        
        endpoint = "https://api.bing.microsoft.com/v7.0/images/search"
        headers = {"Ocp-Apim-Subscription-Key": _subscription_key}
        params = {
            "q": query,
            "count": min(max_results, 150),
            "mkt": market
        }
        
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        results = []
        
        if "value" in data:
            for item in data["value"]:
                results.append({
                    "title": item.get("name", ""),
                    "url": item.get("contentUrl", ""),
                    "thumbnail": item.get("thumbnailUrl", ""),
                    "source": item.get("hostPageUrl", "")
                })
        
        return {
            "results": results,
            "count": len(results),
            "query": query,
            "provider": "Bing Images"
        }
    except Exception as e:
        error_msg = f"Bing image search failed: {e}"
        logger.error(error_msg)
        return {"error": error_msg}


def search_videos(query: str, max_results: int = 10, market: str = "en-US") -> Dict[str, Any]:
    """
    Search for videos using Bing Video Search API.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return (default: 10, max: 105)
        market: Market code for localized results (default: "en-US")
    
    Returns:
        Dictionary with 'results' key containing list of video results.
        Each result has 'title', 'url', 'duration', 'publisher' keys.
        On error, returns dict with 'error' key.
    """
    global _subscription_key, _initialized
    
    if not _initialized:
        init_result = init_tools_library()
        if init_result.get("status") == "error":
            return init_result
    
    try:
        import requests
        
        endpoint = "https://api.bing.microsoft.com/v7.0/videos/search"
        headers = {"Ocp-Apim-Subscription-Key": _subscription_key}
        params = {
            "q": query,
            "count": min(max_results, 105),
            "mkt": market
        }
        
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        results = []
        
        if "value" in data:
            for item in data["value"]:
                results.append({
                    "title": item.get("name", ""),
                    "url": item.get("contentUrl", ""),
                    "duration": item.get("duration", ""),
                    "publisher": item.get("publisher", [{}])[0].get("name", "")
                })
        
        return {
            "results": results,
            "count": len(results),
            "query": query,
            "provider": "Bing Videos"
        }
    except Exception as e:
        error_msg = f"Bing video search failed: {e}"
        logger.error(error_msg)
        return {"error": error_msg}


# LCP Tool Discovery Metadata
__tools__ = [
    {
        "name": "search_web",
        "description": "Search the web using Bing Search API (requires API key, free tier: 1000/month)",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query string"
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of results to return (max: 50)",
                    "default": 10
                },
                "market": {
                    "type": "string",
                    "description": "Market code for localized results (e.g., 'en-US', 'en-GB', 'es-ES')",
                    "default": "en-US"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "search_news",
        "description": "Search for news articles using Bing News Search API",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query string"
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of results to return (max: 100)",
                    "default": 10
                },
                "market": {
                    "type": "string",
                    "description": "Market code for localized results",
                    "default": "en-US"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "search_images",
        "description": "Search for images using Bing Image Search API",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query string"
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of results to return (max: 150)",
                    "default": 10
                },
                "market": {
                    "type": "string",
                    "description": "Market code for localized results",
                    "default": "en-US"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "search_videos",
        "description": "Search for videos using Bing Video Search API",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query string"
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of results to return (max: 105)",
                    "default": 10
                },
                "market": {
                    "type": "string",
                    "description": "Market code for localized results",
                    "default": "en-US"
                }
            },
            "required": ["query"]
        }
    }
]