"""
Google Scholar Tools for LCP

This module provides tools for searching and retrieving academic papers from Google Scholar.
It uses web scraping techniques to extract paper information without requiring API keys.

Tools:
    - search_google_scholar: Search for papers on Google Scholar
    - get_scholar_citations: Get citation count for a paper
    - get_scholar_profile: Get author profile information
    - search_scholar_by_author: Search papers by author name

Note: Google Scholar has rate limits. Use responsibly to avoid IP blocking.
"""

import re
import time
from typing import Dict, List, Optional, Any
from urllib.parse import quote_plus, urljoin
import json

# Global state for lazy initialization
_session = None
_initialized = False


def init_tools_library() -> Dict[str, Any]:
    """
    Initialize the Google Scholar tools library.
    
    This function is called by LCP on first tool invocation.
    It sets up the HTTP session with appropriate headers.
    
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
        
        # Set headers to mimic browser
        _session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
        _initialized = True
        
        return {
            "success": True,
            "message": "Google Scholar tools initialized successfully",
            "rate_limit_warning": "Google Scholar has rate limits. Use responsibly."
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


def _parse_scholar_results(html: str) -> List[Dict[str, Any]]:
    """
    Parse Google Scholar search results HTML.
    
    Args:
        html: Raw HTML from Google Scholar search
        
    Returns:
        List of parsed paper dictionaries
    """
    from html.parser import HTMLParser
    
    papers = []
    
    # Simple regex-based parsing (more robust than full HTML parsing for Scholar)
    # Find all result blocks
    result_pattern = r'<div class="gs_r gs_or gs_scl".*?</div>\s*</div>\s*</div>'
    results = re.findall(result_pattern, html, re.DOTALL)
    
    for result in results:
        paper = {}
        
        # Extract title
        title_match = re.search(r'<h3 class="gs_rt".*?>(.*?)</h3>', result, re.DOTALL)
        if title_match:
            title = re.sub(r'<[^>]+>', '', title_match.group(1))
            paper['title'] = title.strip()
        
        # Extract authors and publication info
        info_match = re.search(r'<div class="gs_a">(.*?)</div>', result, re.DOTALL)
        if info_match:
            info_text = re.sub(r'<[^>]+>', '', info_match.group(1))
            paper['authors_venue'] = info_text.strip()
            
            # Try to extract year
            year_match = re.search(r'\b(19|20)\d{2}\b', info_text)
            if year_match:
                paper['year'] = year_match.group(0)
        
        # Extract snippet/abstract
        snippet_match = re.search(r'<div class="gs_rs">(.*?)</div>', result, re.DOTALL)
        if snippet_match:
            snippet = re.sub(r'<[^>]+>', '', snippet_match.group(1))
            paper['snippet'] = snippet.strip()
        
        # Extract citation count
        cite_match = re.search(r'Cited by (\d+)', result)
        if cite_match:
            paper['citations'] = int(cite_match.group(1))
        else:
            paper['citations'] = 0
        
        # Extract PDF link if available
        pdf_match = re.search(r'<a href="([^"]+\.pdf[^"]*)"', result)
        if pdf_match:
            paper['pdf_link'] = pdf_match.group(1)
        
        # Extract Scholar link
        link_match = re.search(r'<h3 class="gs_rt".*?><a href="([^"]+)"', result, re.DOTALL)
        if link_match:
            paper['scholar_link'] = urljoin('https://scholar.google.com', link_match.group(1))
        
        if paper.get('title'):
            papers.append(paper)
    
    return papers


def tool_search_google_scholar(
    query: str,
    num_results: int = 10,
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
    sort_by: str = "relevance"
) -> Dict[str, Any]:
    """
    Search Google Scholar for academic papers.
    
    Args:
        query: Search query string
        num_results: Number of results to return (max 20)
        year_from: Filter papers from this year onwards
        year_to: Filter papers up to this year
        sort_by: Sort order - "relevance" or "date"
        
    Returns:
        dict: Search results with paper information
        
    Example:
        >>> result = tool_search_google_scholar("machine learning", num_results=5)
        >>> for paper in result['papers']:
        ...     print(paper['title'], paper['citations'])
    """
    _ensure_initialized()
    
    try:
        # Build search URL
        base_url = "https://scholar.google.com/scholar"
        params = {
            'q': query,
            'hl': 'en',
            'num': min(num_results, 20)
        }
        
        if year_from:
            params['as_ylo'] = year_from
        if year_to:
            params['as_yhi'] = year_to
        if sort_by == "date":
            params['scisbd'] = '1'
        
        # Make request
        response = _session.get(base_url, params=params, timeout=30)
        response.raise_for_status()
        
        # Parse results
        papers = _parse_scholar_results(response.text)
        
        return {
            "success": True,
            "query": query,
            "num_results": len(papers),
            "papers": papers[:num_results],
            "filters": {
                "year_from": year_from,
                "year_to": year_to,
                "sort_by": sort_by
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Search failed: {str(e)}",
            "query": query
        }


def tool_get_scholar_citations(title: str, author: Optional[str] = None) -> Dict[str, Any]:
    """
    Get citation count for a specific paper.
    
    Args:
        title: Paper title
        author: Optional author name to narrow search
        
    Returns:
        dict: Citation information
        
    Example:
        >>> result = tool_get_scholar_citations("Attention is all you need", "Vaswani")
        >>> print(f"Citations: {result['citations']}")
    """
    _ensure_initialized()
    
    try:
        # Search for the paper
        query = f'"{title}"'
        if author:
            query += f' author:"{author}"'
        
        result = tool_search_google_scholar(query, num_results=1)
        
        if not result.get("success"):
            return result
        
        papers = result.get("papers", [])
        if not papers:
            return {
                "success": False,
                "error": "Paper not found",
                "title": title
            }
        
        paper = papers[0]
        
        return {
            "success": True,
            "title": paper.get("title"),
            "citations": paper.get("citations", 0),
            "year": paper.get("year"),
            "scholar_link": paper.get("scholar_link")
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Citation lookup failed: {str(e)}",
            "title": title
        }


def tool_search_scholar_by_author(
    author_name: str,
    num_results: int = 10,
    sort_by: str = "citations"
) -> Dict[str, Any]:
    """
    Search for papers by a specific author.
    
    Args:
        author_name: Author's name
        num_results: Number of results to return
        sort_by: Sort order - "citations" or "date"
        
    Returns:
        dict: Author's papers sorted by citations or date
        
    Example:
        >>> result = tool_search_scholar_by_author("Yann LeCun", num_results=5)
        >>> for paper in result['papers']:
        ...     print(paper['title'], paper['citations'])
    """
    _ensure_initialized()
    
    try:
        # Search with author filter
        query = f'author:"{author_name}"'
        
        result = tool_search_google_scholar(query, num_results=num_results * 2)
        
        if not result.get("success"):
            return result
        
        papers = result.get("papers", [])
        
        # Sort by citations if requested
        if sort_by == "citations":
            papers.sort(key=lambda x: x.get("citations", 0), reverse=True)
        
        return {
            "success": True,
            "author": author_name,
            "num_results": len(papers[:num_results]),
            "papers": papers[:num_results],
            "sort_by": sort_by
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Author search failed: {str(e)}",
            "author": author_name
        }


def tool_get_scholar_profile(author_name: str, affiliation: Optional[str] = None) -> Dict[str, Any]:
    """
    Get Google Scholar profile information for an author.
    
    Args:
        author_name: Author's full name
        affiliation: Optional affiliation to narrow search
        
    Returns:
        dict: Profile information including h-index, total citations
        
    Example:
        >>> result = tool_get_scholar_profile("Geoffrey Hinton", "University of Toronto")
        >>> print(f"h-index: {result['h_index']}")
    """
    _ensure_initialized()
    
    try:
        # Search for author profile
        query = author_name
        if affiliation:
            query += f" {affiliation}"
        
        # Use citations search to find profile
        base_url = "https://scholar.google.com/citations"
        params = {
            'view_op': 'search_authors',
            'mauthors': query,
            'hl': 'en'
        }
        
        response = _session.get(base_url, params=params, timeout=30)
        response.raise_for_status()
        
        # Parse profile information
        html = response.text
        
        # Extract profile link
        profile_match = re.search(r'<a href="(/citations\?user=[^"]+)"', html)
        if not profile_match:
            return {
                "success": False,
                "error": "Profile not found",
                "author": author_name
            }
        
        profile_url = urljoin('https://scholar.google.com', profile_match.group(1))
        
        # Get profile page
        profile_response = _session.get(profile_url, timeout=30)
        profile_response.raise_for_status()
        profile_html = profile_response.text
        
        # Extract metrics
        h_index_match = re.search(r'h-index</td>\s*<td[^>]*>(\d+)', profile_html)
        i10_index_match = re.search(r'i10-index</td>\s*<td[^>]*>(\d+)', profile_html)
        citations_match = re.search(r'Citations</td>\s*<td[^>]*>(\d+)', profile_html)
        
        # Extract affiliation
        affil_match = re.search(r'<div class="gsc_prf_il">(.*?)</div>', profile_html)
        affiliation_text = re.sub(r'<[^>]+>', '', affil_match.group(1)) if affil_match else None
        
        return {
            "success": True,
            "author": author_name,
            "affiliation": affiliation_text,
            "h_index": int(h_index_match.group(1)) if h_index_match else None,
            "i10_index": int(i10_index_match.group(1)) if i10_index_match else None,
            "total_citations": int(citations_match.group(1)) if citations_match else None,
            "profile_url": profile_url
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Profile lookup failed: {str(e)}",
            "author": author_name
        }


# Tool metadata for LCP discovery
__tools__ = [
    {
        "name": "search_google_scholar",
        "description": "Search Google Scholar for academic papers with filters",
        "category": "academic_search"
    },
    {
        "name": "get_scholar_citations",
        "description": "Get citation count for a specific paper",
        "category": "citation_analysis"
    },
    {
        "name": "search_scholar_by_author",
        "description": "Search papers by author name",
        "category": "author_search"
    },
    {
        "name": "get_scholar_profile",
        "description": "Get author profile with h-index and metrics",
        "category": "author_metrics"
    }
]