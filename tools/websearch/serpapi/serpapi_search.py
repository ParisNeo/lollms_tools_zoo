"""
SerpAPI toolset for LCP.

This module provides web search capabilities using SerpAPI, which supports
multiple search engines including Google, Bing, Yahoo, and DuckDuckGo.
"""

import os
import requests
from typing import Dict, List, Optional, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables for lazy initialization
_serpapi_key = None

def init_tools_library() -> Dict[str, Any]:
    """
    Initialize the SerpAPI tools library.
    
    This function is called by LCP on first tool invocation.
    It validates API credentials and sets up the search service.
    
    Returns:
        Dict[str, Any]: Initialization status and metadata
    """
    global _serpapi_key
    
    try:
        # Get API key from environment
        _serpapi_key = os.getenv('SERPAPI_KEY')
        
        if not _serpapi_key:
            return {
                "status": "error",
                "error": "SERPAPI_KEY environment variable not set. Please set your SerpAPI key."
            }
        
        # Test API connection
        test_url = "https://serpapi.com/search"
        test_params = {
            'api_key': _serpapi_key,
            'engine': 'google',
            'q': 'test',
            'num': 1
        }
        
        response = requests.get(test_url, params=test_params, timeout=10)
        response.raise_for_status()
        
        logger.info("SerpAPI initialized successfully")
        
        return {
            "status": "success",
            "message": "SerpAPI tools initialized successfully",
            "api_key_set": bool(_serpapi_key)
        }
        
    except requests.exceptions.RequestException as e:
        error_msg = f"Failed to connect to SerpAPI: {str(e)}"
        logger.error(error_msg)
        return {
            "status": "error",
            "error": error_msg
        }
    except Exception as e:
        error_msg = f"Unexpected error during SerpAPI initialization: {str(e)}"
        logger.error(error_msg)
        return {
            "status": "error",
            "error": error_msg
        }

def serpapi_google_search(query: str, num_results: int = 10, start_index: int = 1,
                         location: str = "United States", language: str = "en",
                         safe_search: str = "active") -> Dict[str, Any]:
    """
    Perform a Google search using SerpAPI.
    
    Args:
        query (str): The search query
        num_results (int): Number of results to return (1-100, default: 10)
        start_index (int): Starting index for results (default: 1)
        location (str): Location for search (default: "United States")
        language (str): Language code (default: "en")
        safe_search (str): Safe search setting ("active", "off", default: "active")
    
    Returns:
        Dict[str, Any]: Search results with metadata
    """
    try:
        if not _serpapi_key:
            return {
                "status": "error",
                "error": "SerpAPI not initialized. Call init_tools_library() first."
            }
        
        # Validate parameters
        if not query.strip():
            return {
                "status": "error",
                "error": "Query cannot be empty"
            }
        
        if not 1 <= num_results <= 100:
            return {
                "status": "error",
                "error": "num_results must be between 1 and 100"
            }
        
        # Prepare search parameters
        search_params = {
            'api_key': _serpapi_key,
            'engine': 'google',
            'q': query,
            'num': num_results,
            'start': start_index,
            'location': location,
            'hl': language,
            'safe': safe_search
        }
        
        # Perform search
        url = "https://serpapi.com/search"
        response = requests.get(url, params=search_params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract search results
        results = []
        if 'organic_results' in data:
            for item in data['organic_results']:
                result = {
                    'title': item.get('title', ''),
                    'url': item.get('link', ''),
                    'snippet': item.get('snippet', ''),
                    'display_url': item.get('displayed_link', ''),
                    'position': item.get('position', 0),
                    'date': item.get('date', ''),
                    'sitelinks': item.get('sitelinks', []),
                    'rich_snippet': item.get('rich_snippet', {}),
                    'thumbnail': item.get('thumbnail', '')
                }
                results.append(result)
        
        # Extract search information
        search_info = data.get('search_information', {})
        
        return {
            "status": "success",
            "data": {
                "query": query,
                "total_results": search_info.get('total_results', 0),
                "search_time": search_info.get('time_taken_displayed', 0),
                "formatted_total_results": search_info.get('total_results_formatted', '0'),
                "results": results,
                "num_results": len(results),
                "start_index": start_index,
                "location": location,
                "language": language,
                "safe_search": safe_search,
                "engine": "google"
            }
        }
        
    except requests.exceptions.RequestException as e:
        error_msg = f"SerpAPI Google search request failed: {str(e)}"
        logger.error(error_msg)
        return {
            "status": "error",
            "error": error_msg
        }
    except Exception as e:
        error_msg = f"Unexpected error during SerpAPI Google search: {str(e)}"
        logger.error(error_msg)
        return {
            "status": "error",
            "error": error_msg
        }

def serpapi_bing_search(query: str, num_results: int = 10, start_index: int = 1,
                       location: str = "United States", language: str = "en",
                       safe_search: str = "moderate") -> Dict[str, Any]:
    """
    Perform a Bing search using SerpAPI.
    
    Args:
        query (str): The search query
        num_results (int): Number of results to return (1-50, default: 10)
        start_index (int): Starting index for results (default: 1)
        location (str): Location for search (default: "United States")
        language (str): Language code (default: "en")
        safe_search (str): Safe search setting ("strict", "moderate", "off", default: "moderate")
    
    Returns:
        Dict[str, Any]: Search results with metadata
    """
    try:
        if not _serpapi_key:
            return {
                "status": "error",
                "error": "SerpAPI not initialized. Call init_tools_library() first."
            }
        
        # Validate parameters
        if not query.strip():
            return {
                "status": "error",
                "error": "Query cannot be empty"
            }
        
        if not 1 <= num_results <= 50:
            return {
                "status": "error",
                "error": "num_results must be between 1 and 50"
            }
        
        # Prepare search parameters
        search_params = {
            'api_key': _serpapi_key,
            'engine': 'bing',
            'q': query,
            'count': num_results,
            'first': start_index,
            'location': location,
            'setlang': language,
            'safesearch': safe_search
        }
        
        # Perform search
        url = "https://serpapi.com/search"
        response = requests.get(url, params=search_params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract search results
        results = []
        if 'organic_results' in data:
            for item in data['organic_results']:
                result = {
                    'title': item.get('title', ''),
                    'url': item.get('link', ''),
                    'snippet': item.get('snippet', ''),
                    'display_url': item.get('displayed_link', ''),
                    'position': item.get('position', 0),
                    'date': item.get('date', ''),
                    'sitelinks': item.get('sitelinks', []),
                    'rich_snippet': item.get('rich_snippet', {}),
                    'thumbnail': item.get('thumbnail', '')
                }
                results.append(result)
        
        # Extract search information
        search_info = data.get('search_information', {})
        
        return {
            "status": "success",
            "data": {
                "query": query,
                "total_results": search_info.get('total_results', 0),
                "search_time": search_info.get('time_taken_displayed', 0),
                "formatted_total_results": search_info.get('total_results_formatted', '0'),
                "results": results,
                "num_results": len(results),
                "start_index": start_index,
                "location": location,
                "language": language,
                "safe_search": safe_search,
                "engine": "bing"
            }
        }
        
    except requests.exceptions.RequestException as e:
        error_msg = f"SerpAPI Bing search request failed: {str(e)}"
        logger.error(error_msg)
        return {
            "status": "error",
            "error": error_msg
        }
    except Exception as e:
        error_msg = f"Unexpected error during SerpAPI Bing search: {str(e)}"
        logger.error(error_msg)
        return {
            "status": "error",
            "error": error_msg
        }

def serpapi_duckduckgo_search(query: str, num_results: int = 10, start_index: int = 1,
                             region: str = "us-en", safe_search: str = "moderate") -> Dict[str, Any]:
    """
    Perform a DuckDuckGo search using SerpAPI.
    
    Args:
        query (str): The search query
        num_results (int): Number of results to return (1-30, default: 10)
        start_index (int): Starting index for results (default: 1)
        region (str): Region for search (default: "us-en")
        safe_search (str): Safe search setting ("strict", "moderate", "off", default: "moderate")
    
    Returns:
        Dict[str, Any]: Search results with metadata
    """
    try:
        if not _serpapi_key:
            return {
                "status": "error",
                "error": "SerpAPI not initialized. Call init_tools_library() first."
            }
        
        # Validate parameters
        if not query.strip():
            return {
                "status": "error",
                "error": "Query cannot be empty"
            }
        
        if not 1 <= num_results <= 30:
            return {
                "status": "error",
                "error": "num_results must be between 1 and 30"
            }
        
        # Prepare search parameters
        search_params = {
            'api_key': _serpapi_key,
            'engine': 'duckduckgo',
            'q': query,
            'kl': region,
            'safe': safe_search
        }
        
        # Perform search
        url = "https://serpapi.com/search"
        response = requests.get(url, params=search_params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract search results
        results = []
        if 'organic_results' in data:
            for item in data['organic_results']:
                result = {
                    'title': item.get('title', ''),
                    'url': item.get('link', ''),
                    'snippet': item.get('snippet', ''),
                    'display_url': item.get('displayed_link', ''),
                    'position': item.get('position', 0),
                    'date': item.get('date', ''),
                    'sitelinks': item.get('sitelinks', []),
                    'rich_snippet': item.get('rich_snippet', {}),
                    'thumbnail': item.get('thumbnail', '')
                }
                results.append(result)
        
        # Extract search information
        search_info = data.get('search_information', {})
        
        return {
            "status": "success",
            "data": {
                "query": query,
                "total_results": search_info.get('total_results', 0),
                "search_time": search_info.get('time_taken_displayed', 0),
                "formatted_total_results": search_info.get('total_results_formatted', '0'),
                "results": results,
                "num_results": len(results),
                "start_index": start_index,
                "region": region,
                "safe_search": safe_search,
                "engine": "duckduckgo"
            }
        }
        
    except requests.exceptions.RequestException as e:
        error_msg = f"SerpAPI DuckDuckGo search request failed: {str(e)}"
        logger.error(error_msg)
        return {
            "status": "error",
            "error": error_msg
        }
    except Exception as e:
        error_msg = f"Unexpected error during SerpAPI DuckDuckGo search: {str(e)}"
        logger.error(error_msg)
        return {
            "status": "error",
            "error": error_msg
        }

def serpapi_image_search(query: str, engine: str = "google", num_results: int = 10,
                        start_index: int = 1, location: str = "United States",
                        language: str = "en", safe_search: str = "active") -> Dict[str, Any]:
    """
    Perform an image search using SerpAPI.
    
    Args:
        query (str): The search query
        engine (str): Search engine ("google", "bing", "yahoo", default: "google")
        num_results (int): Number of results to return (1-100, default: 10)
        start_index (int): Starting index for results (default: 1)
        location (str): Location for search (default: "United States")
        language (str): Language code (default: "en")
        safe_search (str): Safe search setting ("active", "off", default: "active")
    
    Returns:
        Dict[str, Any]: Image search results with metadata
    """
    try:
        if not _serpapi_key:
            return {
                "status": "error",
                "error": "SerpAPI not initialized. Call init_tools_library() first."
            }
        
        # Validate parameters
        if not query.strip():
            return {
                "status": "error",
                "error": "Query cannot be empty"
            }
        
        if not 1 <= num_results <= 100:
            return {
                "status": "error",
                "error": "num_results must be between 1 and 100"
            }
        
        if engine not in ["google", "bing", "yahoo"]:
            return {
                "status": "error",
                "error": "engine must be one of: google, bing, yahoo"
            }
        
        # Prepare search parameters
        search_params = {
            'api_key': _serpapi_key,
            'engine': f'{engine}_images',
            'q': query,
            'num': num_results,
            'start': start_index,
            'location': location,
            'hl': language,
            'safe': safe_search
        }
        
        # Perform search
        url = "https://serpapi.com/search"
        response = requests.get(url, params=search_params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract image results
        results = []
        if 'images_results' in data:
            for item in data['images_results']:
                result = {
                    'title': item.get('title', ''),
                    'url': item.get('link', ''),
                    'image_url': item.get('original', ''),
                    'thumbnail_url': item.get('thumbnail', ''),
                    'source': item.get('source', ''),
                    'position': item.get('position', 0),
                    'width': item.get('original_width', 0),
                    'height': item.get('original_height', 0),
                    'thumbnail_width': item.get('thumbnail_width', 0),
                    'thumbnail_height': item.get('thumbnail_height', 0)
                }
                results.append(result)
        
        # Extract search information
        search_info = data.get('search_information', {})
        
        return {
            "status": "success",
            "data": {
                "query": query,
                "total_results": search_info.get('total_results', 0),
                "search_time": search_info.get('time_taken_displayed', 0),
                "formatted_total_results": search_info.get('total_results_formatted', '0'),
                "results": results,
                "num_results": len(results),
                "start_index": start_index,