"""
Google Custom Search toolset for LCP.

This module provides web search capabilities using Google Custom Search API.
Requires API key and Search Engine ID from Google Cloud Console.
"""

import os
import requests
from typing import Dict, List, Optional, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables for lazy initialization
_google_service = None
_api_key = None
_search_engine_id = None

def init_tools_library() -> Dict[str, Any]:
    """
    Initialize the Google Custom Search tools library.
    
    This function is called by LCP on first tool invocation.
    It validates API credentials and sets up the search service.
    
    Returns:
        Dict[str, Any]: Initialization status and metadata
    """
    global _google_service, _api_key, _search_engine_id
    
    try:
        # Get API credentials from environment
        _api_key = os.getenv('GOOGLE_API_KEY')
        _search_engine_id = os.getenv('GOOGLE_SEARCH_ENGINE_ID')
        
        if not _api_key:
            return {
                "status": "error",
                "error": "GOOGLE_API_KEY environment variable not set. Please set your Google API key."
            }
        
        if not _search_engine_id:
            return {
                "status": "error", 
                "error": "GOOGLE_SEARCH_ENGINE_ID environment variable not set. Please set your Google Search Engine ID."
            }
        
        # Test API connection
        test_url = "https://www.googleapis.com/customsearch/v1"
        test_params = {
            'key': _api_key,
            'cx': _search_engine_id,
            'q': 'test',
            'num': 1
        }
        
        response = requests.get(test_url, params=test_params, timeout=10)
        response.raise_for_status()
        
        logger.info("Google Custom Search API initialized successfully")
        
        return {
            "status": "success",
            "message": "Google Custom Search tools initialized successfully",
            "api_key_set": bool(_api_key),
            "search_engine_id_set": bool(_search_engine_id)
        }
        
    except requests.exceptions.RequestException as e:
        error_msg = f"Failed to connect to Google Custom Search API: {str(e)}"
        logger.error(error_msg)
        return {
            "status": "error",
            "error": error_msg
        }
    except Exception as e:
        error_msg = f"Unexpected error during Google Search initialization: {str(e)}"
        logger.error(error_msg)
        return {
            "status": "error",
            "error": error_msg
        }

def google_web_search(query: str, num_results: int = 10, start_index: int = 1, 
                     safe_search: str = "medium", language: str = "en") -> Dict[str, Any]:
    """
    Perform a web search using Google Custom Search API.
    
    Args:
        query (str): The search query
        num_results (int): Number of results to return (1-10, default: 10)
        start_index (int): Starting index for results (default: 1)
        safe_search (str): Safe search setting ("off", "medium", "high", default: "medium")
        language (str): Language code (default: "en")
    
    Returns:
        Dict[str, Any]: Search results with metadata
    """
    try:
        if not _api_key or not _search_engine_id:
            return {
                "status": "error",
                "error": "Google Search not initialized. Call init_tools_library() first."
            }
        
        # Validate parameters
        if not query.strip():
            return {
                "status": "error",
                "error": "Query cannot be empty"
            }
        
        if not 1 <= num_results <= 10:
            return {
                "status": "error",
                "error": "num_results must be between 1 and 10"
            }
        
        if start_index < 1:
            return {
                "status": "error",
                "error": "start_index must be >= 1"
            }
        
        # Prepare search parameters
        search_params = {
            'key': _api_key,
            'cx': _search_engine_id,
            'q': query,
            'num': num_results,
            'start': start_index,
            'safe': safe_search,
            'hl': language
        }
        
        # Perform search
        url = "https://www.googleapis.com/customsearch/v1"
        response = requests.get(url, params=search_params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract search results
        results = []
        if 'items' in data:
            for item in data['items']:
                result = {
                    'title': item.get('title', ''),
                    'url': item.get('link', ''),
                    'snippet': item.get('snippet', ''),
                    'display_url': item.get('displayLink', ''),
                    'formatted_url': item.get('formattedUrl', ''),
                    'html_snippet': item.get('htmlSnippet', ''),
                    'cache_id': item.get('cacheId', ''),
                    'breadcrumb': item.get('breadcrumb', {})
                }
                results.append(result)
        
        # Extract search information
        search_info = data.get('searchInformation', {})
        
        return {
            "status": "success",
            "data": {
                "query": query,
                "total_results": search_info.get('totalResults', '0'),
                "search_time": search_info.get('searchTime', 0),
                "formatted_total_results": search_info.get('formattedTotalResults', '0'),
                "formatted_search_time": search_info.get('formattedSearchTime', '0'),
                "results": results,
                "num_results": len(results),
                "start_index": start_index,
                "safe_search": safe_search,
                "language": language
            }
        }
        
    except requests.exceptions.RequestException as e:
        error_msg = f"Google Search API request failed: {str(e)}"
        logger.error(error_msg)
        return {
            "status": "error",
            "error": error_msg
        }
    except Exception as e:
        error_msg = f"Unexpected error during Google search: {str(e)}"
        logger.error(error_msg)
        return {
            "status": "error",
            "error": error_msg
        }

def google_image_search(query: str, num_results: int = 10, start_index: int = 1,
                       safe_search: str = "medium", image_size: str = "medium",
                       image_type: str = "photo") -> Dict[str, Any]:
    """
    Perform an image search using Google Custom Search API.
    
    Args:
        query (str): The search query
        num_results (int): Number of results to return (1-10, default: 10)
        start_index (int): Starting index for results (default: 1)
        safe_search (str): Safe search setting ("off", "medium", "high", default: "medium")
        image_size (str): Image size ("small", "medium", "large", "xlarge", "xxlarge", "huge", default: "medium")
        image_type (str): Image type ("clipart", "face", "lineart", "news", "photo", default: "photo")
    
    Returns:
        Dict[str, Any]: Image search results with metadata
    """
    try:
        if not _api_key or not _search_engine_id:
            return {
                "status": "error",
                "error": "Google Search not initialized. Call init_tools_library() first."
            }
        
        # Validate parameters
        if not query.strip():
            return {
                "status": "error",
                "error": "Query cannot be empty"
            }
        
        if not 1 <= num_results <= 10:
            return {
                "status": "error",
                "error": "num_results must be between 1 and 10"
            }
        
        # Prepare search parameters
        search_params = {
            'key': _api_key,
            'cx': _search_engine_id,
            'q': query,
            'num': num_results,
            'start': start_index,
            'safe': safe_search,
            'searchType': 'image',
            'imgSize': image_size,
            'imgType': image_type
        }
        
        # Perform search
        url = "https://www.googleapis.com/customsearch/v1"
        response = requests.get(url, params=search_params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract image results
        results = []
        if 'items' in data:
            for item in data['items']:
                result = {
                    'title': item.get('title', ''),
                    'url': item.get('link', ''),
                    'snippet': item.get('snippet', ''),
                    'display_url': item.get('displayLink', ''),
                    'image_url': item.get('link', ''),
                    'thumbnail_url': item.get('image', {}).get('thumbnailLink', ''),
                    'image_width': item.get('image', {}).get('width', 0),
                    'image_height': item.get('image', {}).get('height', 0),
                    'image_size': item.get('image', {}).get('byteSize', 0),
                    'mime_type': item.get('mime', ''),
                    'file_format': item.get('fileFormat', '')
                }
                results.append(result)
        
        # Extract search information
        search_info = data.get('searchInformation', {})
        
        return {
            "status": "success",
            "data": {
                "query": query,
                "total_results": search_info.get('totalResults', '0'),
                "search_time": search_info.get('searchTime', 0),
                "formatted_total_results": search_info.get('formattedTotalResults', '0'),
                "formatted_search_time": search_info.get('formattedSearchTime', '0'),
                "results": results,
                "num_results": len(results),
                "start_index": start_index,
                "safe_search": safe_search,
                "image_size": image_size,
                "image_type": image_type
            }
        }
        
    except requests.exceptions.RequestException as e:
        error_msg = f"Google Image Search API request failed: {str(e)}"
        logger.error(error_msg)
        return {
            "status": "error",
            "error": error_msg
        }
    except Exception as e:
        error_msg = f"Unexpected error during Google image search: {str(e)}"
        logger.error(error_msg)
        return {
            "status": "error",
            "error": error_msg
        }

# LCP Tools Metadata
__tools__ = [
    {
        "name": "google_web_search",
        "description": "Perform a web search using Google Custom Search API",
        "parameters": {
            "query": {"type": "string", "description": "The search query", "required": True},
            "num_results": {"type": "integer", "description": "Number of results to return (1-10)", "default": 10},
            "start_index": {"type": "integer", "description": "Starting index for results", "default": 1},
            "safe_search": {"type": "string", "description": "Safe search setting", "default": "medium"},
            "language": {"type": "string", "description": "Language code", "default": "en"}
        }
    },
    {
        "name": "google_image_search",
        "description": "Perform an image search using Google Custom Search API",
        "parameters": {
            "query": {"type": "string", "description": "The search query", "required": True},
            "num_results": {"type": "integer", "description": "Number of results to return (1-10)", "default": 10},
            "start_index": {"type": "integer", "description": "Starting index for results", "default": 1},
            "safe_search": {"type": "string", "description": "Safe search setting", "default": "medium"},
            "image_size": {"type": "string", "description": "Image size", "default": "medium"},
            "image_type": {"type": "string", "description": "Image type", "default": "photo"}
        }
    }
]