"""
CrossRef Tools for LCP

This module provides tools for searching and retrieving academic papers from CrossRef.
CrossRef is the official DOI registration agency and provides comprehensive metadata.

Tools:
    - search_crossref: Search for papers by query
    - get_work_by_doi: Get detailed work information by DOI
    - search_by_author: Search papers by author name
    - search_by_title: Search papers by title
    - get_journal_works: Get works from a specific journal
    - get_funder_works: Get works by funding agency

API Documentation: https://api.crossref.org/
No API key required, but polite pool access requires email in User-Agent
"""

import time
from typing import Dict, List, Optional, Any
from urllib.parse import quote
import json

# Global state for lazy initialization
_session = None
_base_url = "https://api.crossref.org"
_initialized = False
_last_request_time = 0
_min_request_interval = 0.05  # 50ms between requests (polite pool)


def init_tools_library() -> Dict[str, Any]:
    """
    Initialize the CrossRef tools library.
    
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
        
        # Set headers (polite pool requires email)
        _session.headers.update({
            'User-Agent': 'LCP-CrossRef/1.0 (mailto:your-email@example.com)',
            'Accept': 'application/json'
        })
        
        _initialized = True
        
        return {
            "success": True,
            "message": "CrossRef tools initialized successfully",
            "api_base": _base_url,
            "note": "Using polite pool - please configure your email in production"
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
    Make a rate-limited request to the CrossRef API.
    
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


def _format_work(work: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format a CrossRef work into a simplified structure.
    
    Args:
        work: Raw CrossRef work data
        
    Returns:
        dict: Formatted work information
    """
    formatted = {
        'doi': work.get('DOI'),
        'title': work.get('title', [''])[0] if work.get('title') else None,
        'type': work.get('type'),
        'publisher': work.get('publisher'),
        'container_title': work.get('container-title', [''])[0] if work.get('container-title') else None,
    }
    
    # Extract authors
    if 'author' in work:
        authors = []
        for author in work['author']:
            name_parts = []
            if 'given' in author:
                name_parts.append(author['given'])
            if 'family' in author:
                name_parts.append(author['family'])
            if name_parts:
                authors.append(' '.join(name_parts))
        formatted['authors'] = authors
    
    # Extract publication date
    if 'published-print' in work:
        date_parts = work['published-print'].get('date-parts', [[]])[0]
        if date_parts:
            formatted['year'] = date_parts[0]
            formatted['publication_date'] = '-'.join(str(p) for p in date_parts)
    elif 'published-online' in work:
        date_parts = work['published-online'].get('date-parts', [[]])[0]
        if date_parts:
            formatted['year'] = date_parts[0]
            formatted['publication_date'] = '-'.join(str(p) for p in date_parts)
    
    # Extract metrics
    if 'is-referenced-by-count' in work:
        formatted['citation_count'] = work['is-referenced-by-count']
    if 'reference-count' in work:
        formatted['reference_count'] = work['reference-count']
    
    # Extract ISSN/ISBN
    if 'ISSN' in work:
        formatted['issn'] = work['ISSN']
    if 'ISBN' in work:
        formatted['isbn'] = work['ISBN']
    
    # Extract URL
    if 'URL' in work:
        formatted['url'] = work['URL']
    
    # Extract abstract
    if 'abstract' in work:
        formatted['abstract'] = work['abstract']
    
    # Extract subject areas
    if 'subject' in work:
        formatted['subjects'] = work['subject']
    
    return formatted


def tool_search_crossref(
    query: str,
    num_results: int = 10,
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
    work_type: Optional[str] = None
) -> Dict[str, Any]:
    """
    Search CrossRef for academic works.
    
    Args:
        query: Search query string
        num_results: Number of results to return (max 1000)
        year_from: Filter works from this year onwards
        year_to: Filter works up to this year
        work_type: Filter by type (journal-article, book-chapter, etc.)
        
    Returns:
        dict: Search results with work information
        
    Example:
        >>> result = tool_search_crossref("machine learning", num_results=5)
        >>> for work in result['works']:
        ...     print(work['title'], work.get('citation_count'))
    """
    _ensure_initialized()
    
    try:
        # Build query parameters
        params = {
            'query': query,
            'rows': min(num_results, 1000)
        }
        
        # Add filters
        filters = []
        if year_from:
            filters.append(f"from-pub-date:{year_from}-01-01")
        if year_to:
            filters.append(f"until-pub-date:{year_to}-12-31")
        if work_type:
            filters.append(f"type:{work_type}")
        
        if filters:
            params['filter'] = ','.join(filters)
        
        # Make request
        url = f"{_base_url}/works"
        data = _rate_limited_request(url, params)
        
        works = [_format_work(item) for item in data['message']['items']]
        
        return {
            "success": True,
            "query": query,
            "num_results": len(works),
            "total_results": data['message']['total-results'],
            "works": works,
            "filters": {
                "year_from": year_from,
                "year_to": year_to,
                "work_type": work_type
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Search failed: {str(e)}",
            "query": query
        }


def tool_get_work_by_doi(doi: str) -> Dict[str, Any]:
    """
    Get detailed information about a work by its DOI.
    
    Args:
        doi: Digital Object Identifier (e.g., "10.1038/nature14539")
        
    Returns:
        dict: Detailed work information
        
    Example:
        >>> result = tool_get_work_by_doi("10.1038/nature14539")
        >>> print(result['work']['title'])
    """
    _ensure_initialized()
    
    try:
        # Clean DOI
        doi = doi.replace('https://doi.org/', '').replace('http://doi.org/', '')
        
        # Make request
        url = f"{_base_url}/works/{quote(doi)}"
        data = _rate_limited_request(url)
        
        work = _format_work(data['message'])
        
        return {
            "success": True,
            "doi": doi,
            "work": work
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to get work: {str(e)}",
            "doi": doi
        }


def tool_search_by_author(
    author_name: str,
    num_results: int = 10,
    year_from: Optional[int] = None,
    year_to: Optional[int] = None
) -> Dict[str, Any]:
    """
    Search for works by author name.
    
    Args:
        author_name: Author's name (e.g., "Geoffrey Hinton")
        num_results: Number of results to return
        year_from: Filter works from this year onwards
        year_to: Filter works up to this year
        
    Returns:
        dict: Author's works
        
    Example:
        >>> result = tool_search_by_author("Yann LeCun", num_results=5)
        >>> for work in result['works']:
        ...     print(work['title'])
    """
    _ensure_initialized()
    
    try:
        # Build query parameters
        params = {
            'query.author': author_name,
            'rows': min(num_results, 1000)
        }
        
        # Add date filters
        filters = []
        if year_from:
            filters.append(f"from-pub-date:{year_from}-01-01")
        if year_to:
            filters.append(f"until-pub-date:{year_to}-12-31")
        
        if filters:
            params['filter'] = ','.join(filters)
        
        # Make request
        url = f"{_base_url}/works"
        data = _rate_limited_request(url, params)
        
        works = [_format_work(item) for item in data['message']['items']]
        
        return {
            "success": True,
            "author": author_name,
            "num_results": len(works),
            "works": works
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Author search failed: {str(e)}",
            "author": author_name
        }


def tool_search_by_title(
    title: str,
    num_results: int = 10,
    exact_match: bool = False
) -> Dict[str, Any]:
    """
    Search for works by title.
    
    Args:
        title: Paper title
        num_results: Number of results to return
        exact_match: If True, search for exact title match
        
    Returns:
        dict: Matching works
        
    Example:
        >>> result = tool_search_by_title("Attention is all you need", exact_match=True)
        >>> print(result['works'][0]['doi'])
    """
    _ensure_initialized()
    
    try:
        # Build query parameters
        if exact_match:
            params = {
                'query.bibliographic': f'"{title}"',
                'rows': min(num_results, 1000)
            }
        else:
            params = {
                'query.title': title,
                'rows': min(num_results, 1000)
            }
        
        # Make request
        url = f"{_base_url}/works"
        data = _rate_limited_request(url, params)
        
        works = [_format_work(item) for item in data['message']['items']]
        
        return {
            "success": True,
            "title": title,
            "exact_match": exact_match,
            "num_results": len(works),
            "works": works
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Title search failed: {str(e)}",
            "title": title
        }


def tool_get_journal_works(
    issn: str,
    num_results: int = 10,
    year_from: Optional[int] = None,
    year_to: Optional[int] = None
) -> Dict[str, Any]:
    """
    Get works from a specific journal.
    
    Args:
        issn: Journal ISSN (e.g., "0028-0836" for Nature)
        num_results: Number of results to return
        year_from: Filter works from this year onwards
        year_to: Filter works up to this year
        
    Returns:
        dict: Journal works
        
    Example:
        >>> result = tool_get_journal_works("0028-0836", num_results=5, year_from=2023)
        >>> for work in result['works']:
        ...     print(work['title'])
    """
    _ensure_initialized()
    
    try:
        # Build query parameters
        params = {
            'filter': f"issn:{issn}",
            'rows': min(num_results, 1000)
        }
        
        # Add date filters
        filters = [f"issn:{issn}"]
        if year_from:
            filters.append(f"from-pub-date:{year_from}-01-01")
        if year_to:
            filters.append(f"until-pub-date:{year_to}-12-31")
        
        params['filter'] = ','.join(filters)
        
        # Make request
        url = f"{_base_url}/works"
        data = _rate_limited_request(url, params)
        
        works = [_format_work(item) for item in data['message']['items']]
        
        return {
            "success": True,
            "issn": issn,
            "num_results": len(works),
            "works": works
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Journal search failed: {str(e)}",
            "issn": issn
        }


def tool_get_funder_works(
    funder_id: str,
    num_results: int = 10,
    year_from: Optional[int] = None,
    year_to: Optional[int] = None
) -> Dict[str, Any]:
    """
    Get works by funding agency.
    
    Args:
        funder_id: Funder ID (e.g., "100000001" for NSF)
        num_results: Number of results to return
        year_from: Filter works from this year onwards
        year_to: Filter works up to this year
        
    Returns:
        dict: Funded works
        
    Example:
        >>> result = tool_get_funder_works("100000001", num_results=5, year_from=2023)
        >>> for work in result['works']:
        ...     print(work['title'])
    """
    _ensure_initialized()
    
    try:
        # Build query parameters
        filters = [f"funder:{funder_id}"]
        if year_from:
            filters.append(f"from-pub-date:{year_from}-01-01")
        if year_to:
            filters.append(f"until-pub-date:{year_to}-12-31")
        
        params = {
            'filter': ','.join(filters),
            'rows': min(num_results, 1000)
        }
        
        # Make request
        url = f"{_base_url}/works"
        data = _rate_limited_request(url, params)
        
        works = [_format_work(item) for item in data['message']['items']]
        
        return {
            "success": True,
            "funder_id": funder_id,
            "num_results": len(works),
            "works": works
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Funder search failed: {str(e)}",
            "funder_id": funder_id
        }


# Tool metadata for LCP discovery
__tools__ = [
    {
        "name": "search_crossref",
        "description": "Search CrossRef for academic works",
        "category": "academic_search"
    },
    {
        "name": "get_work_by_doi",
        "description": "Get detailed work information by DOI",
        "category": "doi_lookup"
    },
    {
        "name": "search_by_author",
        "description": "Search works by author name",
        "category": "author_search"
    },
    {
        "name": "search_by_title",
        "description": "Search works by title",
        "category": "title_search"
    },
    {
        "name": "get_journal_works",
        "description": "Get works from a specific journal",
        "category": "journal_search"
    },
    {
        "name": "get_funder_works",
        "description": "Get works by funding agency",
        "category": "funder_search"
    }
]