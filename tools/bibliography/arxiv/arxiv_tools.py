"""
arXiv Tools for LCP.

Provides tools for searching and downloading papers from arXiv.
arXiv API is free and does not require authentication.
"""

import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from typing import List, Optional
from pathlib import Path
import json


def init_tools_library() -> dict:
    """
    Initializes the arXiv tools library.
    
    Returns:
        dict: Status dictionary indicating successful initialization.
    """
    return {
        "status": "success",
        "message": "arXiv tools initialized successfully.",
        "tools_count": 4,
        "requires_api_key": False
    }


def tool_search_arxiv(query: str, max_results: int = 10, sort_by: str = "relevance") -> dict:
    """
    Searches arXiv for papers matching the query.

    Args:
        query (str): Search query (e.g., "machine learning", "quantum computing").
        max_results (int): Maximum number of results to return. Defaults to 10.
        sort_by (str): Sort order - "relevance", "lastUpdatedDate", or "submittedDate". Defaults to "relevance".

    Returns:
        dict: Dictionary containing search results with paper metadata.
    """
    try:
        base_url = "http://export.arxiv.org/api/query"
        
        params = {
            "search_query": f"all:{query}",
            "start": 0,
            "max_results": max_results,
            "sortBy": sort_by,
            "sortOrder": "descending"
        }
        
        url = f"{base_url}?{urllib.parse.urlencode(params)}"
        
        with urllib.request.urlopen(url, timeout=30) as response:
            data = response.read()
        
        root = ET.fromstring(data)
        
        # Namespace handling
        ns = {
            'atom': 'http://www.w3.org/2005/Atom',
            'arxiv': 'http://arxiv.org/schemas/atom'
        }
        
        entries = []
        for entry in root.findall('atom:entry', ns):
            paper = {
                "id": entry.find('atom:id', ns).text.split('/abs/')[-1],
                "title": entry.find('atom:title', ns).text.strip().replace('\n', ' '),
                "authors": [author.find('atom:name', ns).text for author in entry.findall('atom:author', ns)],
                "summary": entry.find('atom:summary', ns).text.strip().replace('\n', ' '),
                "published": entry.find('atom:published', ns).text,
                "updated": entry.find('atom:updated', ns).text,
                "pdf_url": entry.find('atom:id', ns).text.replace('/abs/', '/pdf/') + ".pdf",
                "arxiv_url": entry.find('atom:id', ns).text
            }
            
            # Get categories
            categories = [cat.get('term') for cat in entry.findall('atom:category', ns)]
            paper["categories"] = categories
            
            entries.append(paper)
        
        return {
            "success": True,
            "query": query,
            "results_count": len(entries),
            "papers": entries
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Error searching arXiv: {str(e)}"
        }


def tool_get_arxiv_paper(arxiv_id: str) -> dict:
    """
    Gets detailed information about a specific arXiv paper.

    Args:
        arxiv_id (str): arXiv ID (e.g., "2103.12345" or "2103.12345v1").

    Returns:
        dict: Dictionary containing paper metadata.
    """
    try:
        base_url = "http://export.arxiv.org/api/query"
        
        params = {
            "id_list": arxiv_id
        }
        
        url = f"{base_url}?{urllib.parse.urlencode(params)}"
        
        with urllib.request.urlopen(url, timeout=30) as response:
            data = response.read()
        
        root = ET.fromstring(data)
        
        ns = {
            'atom': 'http://www.w3.org/2005/Atom',
            'arxiv': 'http://arxiv.org/schemas/atom'
        }
        
        entry = root.find('atom:entry', ns)
        
        if entry is None:
            return {
                "success": False,
                "error": f"Paper with ID '{arxiv_id}' not found."
            }
        
        paper = {
            "id": entry.find('atom:id', ns).text.split('/abs/')[-1],
            "title": entry.find('atom:title', ns).text.strip().replace('\n', ' '),
            "authors": [author.find('atom:name', ns).text for author in entry.findall('atom:author', ns)],
            "summary": entry.find('atom:summary', ns).text.strip().replace('\n', ' '),
            "published": entry.find('atom:published', ns).text,
            "updated": entry.find('atom:updated', ns).text,
            "pdf_url": entry.find('atom:id', ns).text.replace('/abs/', '/pdf/') + ".pdf",
            "arxiv_url": entry.find('atom:id', ns).text,
            "categories": [cat.get('term') for cat in entry.findall('atom:category', ns)]
        }
        
        # Get DOI if available
        doi_element = entry.find('arxiv:doi', ns)
        if doi_element is not None:
            paper["doi"] = doi_element.text
        
        # Get journal reference if available
        journal_ref = entry.find('arxiv:journal_ref', ns)
        if journal_ref is not None:
            paper["journal_ref"] = journal_ref.text
        
        return {
            "success": True,
            "paper": paper
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Error fetching paper: {str(e)}"
        }


def tool_download_arxiv_pdf(arxiv_id: str, output_path: Optional[str] = None) -> dict:
    """
    Downloads the PDF of an arXiv paper.

    Args:
        arxiv_id (str): arXiv ID (e.g., "2103.12345").
        output_path (Optional[str]): Output file path. If None, saves as "{arxiv_id}.pdf" in current directory.

    Returns:
        dict: Dictionary containing download status and file path.
    """
    try:
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
        
        if output_path is None:
            output_path = f"{arxiv_id.replace('/', '_')}.pdf"
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with urllib.request.urlopen(pdf_url, timeout=60) as response:
            pdf_data = response.read()
        
        output_file.write_bytes(pdf_data)
        
        return {
            "success": True,
            "arxiv_id": arxiv_id,
            "file_path": str(output_file.absolute()),
            "file_size_bytes": len(pdf_data),
            "message": f"PDF downloaded successfully to '{output_path}'"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Error downloading PDF: {str(e)}"
        }


def tool_search_arxiv_by_author(author_name: str, max_results: int = 10) -> dict:
    """
    Searches arXiv for papers by a specific author.

    Args:
        author_name (str): Author name (e.g., "Yann LeCun").
        max_results (int): Maximum number of results to return. Defaults to 10.

    Returns:
        dict: Dictionary containing search results.
    """
    try:
        base_url = "http://export.arxiv.org/api/query"
        
        params = {
            "search_query": f"au:\"{author_name}\"",
            "start": 0,
            "max_results": max_results,
            "sortBy": "submittedDate",
            "sortOrder": "descending"
        }
        
        url = f"{base_url}?{urllib.parse.urlencode(params)}"
        
        with urllib.request.urlopen(url, timeout=30) as response:
            data = response.read()
        
        root = ET.fromstring(data)
        
        ns = {
            'atom': 'http://www.w3.org/2005/Atom',
            'arxiv': 'http://arxiv.org/schemas/atom'
        }
        
        entries = []
        for entry in root.findall('atom:entry', ns):
            paper = {
                "id": entry.find('atom:id', ns).text.split('/abs/')[-1],
                "title": entry.find('atom:title', ns).text.strip().replace('\n', ' '),
                "authors": [author.find('atom:name', ns).text for author in entry.findall('atom:author', ns)],
                "published": entry.find('atom:published', ns).text,
                "arxiv_url": entry.find('atom:id', ns).text
            }
            entries.append(paper)
        
        return {
            "success": True,
            "author": author_name,
            "results_count": len(entries),
            "papers": entries
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Error searching by author: {str(e)}"
        }