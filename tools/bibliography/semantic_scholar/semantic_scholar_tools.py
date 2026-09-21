"""
Semantic Scholar Tools for LCP

This module provides tools for searching and retrieving academic papers from Semantic Scholar.
It uses the official Semantic Scholar API which provides rich metadata and citation graphs.

Tools:
    - search_semantic_scholar: Search for papers
    - get_paper_details: Get detailed paper information
    - get_paper_citations: Get papers that cite a given paper
    - get_paper_references: Get papers referenced by a given paper
    - get_author_papers: Get papers by author
    - get_author_details: Get author information and metrics

API Documentation: https://api.semanticscholar.org/
No API key required for basic usage (rate limited to 100 requests per 5 minutes)
"""

import time
from typing import Dict, List, Optional, Any
import json

# Global state for lazy initialization
_session = None
_base_url = "https://api.semanticscholar.org/graph/v1"
_initialized = False
_last_request_time = 0
_min_request_interval = 0.1  # 100ms between requests to respect rate limits


def init_tools_library() -> Dict[str, Any]:
    """
    Initialize the Semantic Scholar tools library.
    
    This function is called by LCP on first tool invocation.
    It sets up the HTTP session with appropriate headers and rate limiting.
    
    Returns:
        dict: Initialization status and configuration
    """
    global _session, _initialized
    
    try:
        import requests
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry
        
        # Create session with retry strategy
        _session = requests.Session()
        
        # Configure retries
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        _session.mount("http://", adapter)
        _session.mount("https://", adapter)
        
        # Set headers
        _session.headers.update({
            'User-Agent': 'LCP-SemanticScholar/1.0',
            'Accept': 'application/json'
        })
        
        _initialized = True
        
        return {
            "success": True,
            "message": "Semantic Scholar tools initialized successfully",
            "api_base": _base_url,
            "rate_limit": "100 requests per 5 minutes (no API key)"
        }
        
    except ImportError as e:
        return {
            "success": False,
            "error": f"Missing required dependency: {str(e)}",
            "install_command": "pip install requests"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Initialization failed: {str(e)}"
        }


def _ensure_initialized():
    """Ensure the library is initialized before use."""
    global _initialized
    if not _initialized:
        result = init_tools_library()
        if not result.get("success"):
            raise RuntimeError(f"Failed to initialize: {result.get('error')}")


def _rate_limited_request(url: str, params: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Make a rate-limited request to the Semantic Scholar API.
    
    Args:
        url: API endpoint URL
        params: Query parameters
        
    Returns:
        dict: API response JSON
    """
    global _last_request_time
    
    # Enforce rate limiting
    current_time = time.time()
    time_since_last = current_time - _last_request_time
    if time_since_last < _min_request_interval:
        time.sleep(_min_request_interval - time_since_last)
    
    response = _session.get(url, params=params, timeout=30)
    _last_request_time = time.time()
    
    response.raise_for_status()
    return response.json()


def tool_search_semantic_scholar(
    query: str,
    num_results: int = 10,
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
    fields: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Search Semantic Scholar for academic papers.
    
    Args:
        query: Search query string
        num_results: Number of results to return (max 100)
        year_from: Filter papers from this year onwards
        year_to: Filter papers up to this year
        fields: List of fields to return (default: title, authors, year, citations)
        
    Returns:
        dict: Search results with paper information
        
    Example:
        >>> result = tool_search_semantic_scholar("transformer models", num_results=5)
        >>> for paper in result['papers']:
        ...     print(paper['title'], paper['citationCount'])
    """
    _ensure_initialized()
    
    try:
        # Default fields
        if fields is None:
            fields = ['title', 'authors', 'year', 'citationCount', 'abstract', 'url', 'externalIds']
        
        # Build query parameters
        params = {
            'query': query,
            'limit': min(num_results, 100),
            'fields': ','.join(fields)
        }
        
        # Add year filters
        if year_from or year_to:
            year_filter = []
            if year_from:
                year_filter.append(f"{year_from}-")
            if year_to:
                if year_filter:
                    year_filter[0] = f"{year_from}-{year_to}"
                else:
                    year_filter.append(f"-{year_to}")
            params['year'] = year_filter[0]
        
        # Make request
        url = f"{_base_url}/paper/search"
        data = _rate_limited_request(url, params)
        
        papers = data.get('data', [])
        
        return {
            "success": True,
            "query": query,
            "num_results": len(papers),
            "total_results": data.get('total', 0),
            "papers": papers,
            "filters": {
                "year_from": year_from,
                "year_to": year_to
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Search failed: {str(e)}",
            "query": query
        }


def tool_get_paper_details(
    paper_id: str,
    fields: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Get detailed information about a specific paper.
    
    Args:
        paper_id: Paper ID (Semantic Scholar ID, DOI, arXiv ID, or URL)
        fields: List of fields to return
        
    Returns:
        dict: Detailed paper information
        
    Example:
        >>> result = tool_get_paper_details("DOI:10.1038/nature14539")
        >>> print(result['paper']['title'])
    """
    _ensure_initialized()
    
    try:
        # Default fields
        if fields is None:
            fields = [
                'title', 'authors', 'year', 'abstract', 'citationCount',
                'referenceCount', 'influentialCitationCount', 'url',
                'externalIds', 'venue', 'publicationDate', 'journal',
                'openAccessPdf', 'fieldsOfStudy', 's2FieldsOfStudy'
            ]
        
        # Build URL
        url = f"{_base_url}/paper/{paper_id}"
        params = {'fields': ','.join(fields)}
        
        # Make request
        data = _rate_limited_request(url, params)
        
        return {
            "success": True,
            "paper_id": paper_id,
            "paper": data
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to get paper details: {str(e)}",
            "paper_id": paper_id
        }


def tool_get_paper_citations(
    paper_id: str,
    num_results: int = 10,
    fields: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Get papers that cite a given paper.
    
    Args:
        paper_id: Paper ID (Semantic Scholar ID, DOI, arXiv ID, or URL)
        num_results: Number of citing papers to return (max 1000)
        fields: List of fields to return for citing papers
        
    Returns:
        dict: List of citing papers
        
    Example:
        >>> result = tool_get_paper_citations("DOI:10.1038/nature14539", num_results=5)
        >>> for paper in result['citations']:
        ...     print(paper['title'])
    """
    _ensure_initialized()
    
    try:
        # Default fields
        if fields is None:
            fields = ['title', 'authors', 'year', 'citationCount', 'url']
        
        # Build URL
        url = f"{_base_url}/paper/{paper_id}/citations"
        params = {
            'limit': min(num_results, 1000),
            'fields': ','.join(fields)
        }
        
        # Make request
        data = _rate_limited_request(url, params)
        
        citations = [item['citingPaper'] for item in data.get('data', [])]
        
        return {
            "success": True,
            "paper_id": paper_id,
            "num_citations": len(citations),
            "citations": citations
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to get citations: {str(e)}",
            "paper_id": paper_id
        }


def tool_get_paper_references(
    paper_id: str,
    num_results: int = 10,
    fields: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Get papers referenced by a given paper.
    
    Args:
        paper_id: Paper ID (Semantic Scholar ID, DOI, arXiv ID, or URL)
        num_results: Number of referenced papers to return (max 1000)
        fields: List of fields to return for referenced papers
        
    Returns:
        dict: List of referenced papers
        
    Example:
        >>> result = tool_get_paper_references("DOI:10.1038/nature14539", num_results=5)
        >>> for paper in result['references']:
        ...     print(paper['title'])
    """
    _ensure_initialized()
    
    try:
        # Default fields
        if fields is None:
            fields = ['title', 'authors', 'year', 'citationCount', 'url']
        
        # Build URL
        url = f"{_base_url}/paper/{paper_id}/references"
        params = {
            'limit': min(num_results, 1000),
            'fields': ','.join(fields)
        }
        
        # Make request
        data = _rate_limited_request(url, params)
        
        references = [item['citedPaper'] for item in data.get('data', [])]
        
        return {
            "success": True,
            "paper_id": paper_id,
            "num_references": len(references),
            "references": references
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to get references: {str(e)}",
            "paper_id": paper_id
        }


def tool_get_author_papers(
    author_id: str,
    num_results: int = 10,
    fields: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Get papers by a specific author.
    
    Args:
        author_id: Author ID (Semantic Scholar Author ID)
        num_results: Number of papers to return (max 1000)
        fields: List of fields to return for papers
        
    Returns:
        dict: List of author's papers
        
    Example:
        >>> result = tool_get_author_papers("1741101", num_results=5)
        >>> for paper in result['papers']:
        ...     print(paper['title'])
    """
    _ensure_initialized()
    
    try:
        # Default fields
        if fields is None:
            fields = ['title', 'authors', 'year', 'citationCount', 'url']
        
        # Build URL
        url = f"{_base_url}/author/{author_id}/papers"
        params = {
            'limit': min(num_results, 1000),
            'fields': ','.join(fields)
        }
        
        # Make request
        data = _rate_limited_request(url, params)
        
        papers = data.get('data', [])
        
        return {
            "success": True,
            "author_id": author_id,
            "num_papers": len(papers),
            "papers": papers
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to get author papers: {str(e)}",
            "author_id": author_id
        }


def tool_get_author_details(
    author_id: str,
    fields: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Get detailed information about an author.
    
    Args:
        author_id: Author ID (Semantic Scholar Author ID)
        fields: List of fields to return
        
    Returns:
        dict: Author information including metrics
        
    Example:
        >>> result = tool_get_author_details("1741101")
        >>> print(f"h-index: {result['author']['hIndex']}")
    """
    _ensure_initialized()
    
    try:
        # Default fields
        if fields is None:
            fields = [
                'name', 'affiliations', 'homepage', 'paperCount',
                'citationCount', 'hIndex', 'url'
            ]
        
        # Build URL
        url = f"{_base_url}/author/{author_id}"
        params = {'fields': ','.join(fields)}
        
        # Make request
        data = _rate_limited_request(url, params)
        
        return {
            "success": True,
            "author_id": author_id,
            "author": data
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to get author details: {str(e)}",
            "author_id": author_id
        }


def tool_search_authors(
    query: str,
    num_results: int = 10,
    fields: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Search for authors by name.
    
    Args:
        query: Author name search query
        num_results: Number of results to return (max 1000)
        fields: List of fields to return
        
    Returns:
        dict: List of matching authors
        
    Example:
        >>> result = tool_search_authors("Yann LeCun", num_results=5)
        >>> for author in result['authors']:
        ...     print(author['name'], author.get('hIndex'))
    """
    _ensure_initialized()
    
    try:
        # Default fields
        if fields is None:
            fields = ['name', 'affiliations', 'paperCount', 'citationCount', 'hIndex']
        
        # Build URL
        url = f"{_base_url}/author/search"
        params = {
            'query': query,
            'limit': min(num_results, 1000),
            'fields': ','.join(fields)
        }
        
        # Make request
        data = _rate_limited_request(url, params)
        
        authors = data.get('data', [])
        
        return {
            "success": True,
            "query": query,
            "num_results": len(authors),
            "authors": authors
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Author search failed: {str(e)}",
            "query": query
        }


# Tool metadata for LCP discovery
__tools__ = [
    {
        "name": "search_semantic_scholar",
        "description": "Search Semantic Scholar for academic papers",
        "category": "academic_search"
    },
    {
        "name": "get_paper_details",
        "description": "Get detailed paper information by ID",
        "category": "paper_metadata"
    },
    {
        "name": "get_paper_citations",
        "description": "Get papers that cite a given paper",
        "category": "citation_analysis"
    },
    {
        "name": "get_paper_references",
        "description": "Get papers referenced by a given paper",
        "category": "citation_analysis"
    },
    {
        "name": "get_author_papers",
        "description": "Get papers by author ID",
        "category": "author_search"
    },
    {
        "name": "get_author_details",
        "description": "Get author information and metrics",
        "category": "author_metrics"
    },
    {
        "name": "search_authors",
        "description": "Search for authors by name",
        "category": "author_search"
    }
]