"""
DOI and Crossref Tools for LCP.

Provides DOI resolution, metadata fetching from Crossref, and citation formatting.
"""

import os
import json
import urllib.request
import urllib.parse
import urllib.error
from typing import Optional, Dict, Any, List
from pathlib import Path


def init_tools_library() -> dict:
    """
    Initializes the DOI/Crossref toolset.
    
    Returns:
        dict: Status dictionary indicating successful initialization.
    """
    return {
        "status": "success",
        "message": "DOI/Crossref toolset initialized successfully.",
        "tools_count": 6,
        "api_base": "https://api.crossref.org"
    }


def _make_crossref_request(endpoint: str, params: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """
    Makes a request to the Crossref API.
    
    Args:
        endpoint (str): API endpoint (e.g., "works/10.1000/xyz123").
        params (Optional[Dict[str, str]]): Query parameters.
    
    Returns:
        Dict[str, Any]: JSON response or error dictionary.
    """
    base_url = "https://api.crossref.org"
    url = f"{base_url}/{endpoint}"
    
    if params:
        query_string = urllib.parse.urlencode(params)
        url = f"{url}?{query_string}"
    
    # Add polite pool headers
    headers = {
        "User-Agent": "LollmsTools/1.0 (mailto:your-email@example.com)"
    }
    
    try:
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return {
            "success": False,
            "error": f"HTTP Error {e.code}: {e.reason}",
            "status_code": e.code
        }
    except urllib.error.URLError as e:
        return {
            "success": False,
            "error": f"URL Error: {str(e.reason)}"
        }
    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error": f"Invalid JSON response: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }


def tool_resolve_doi(doi: str) -> dict:
    """
    Resolves a DOI and fetches its metadata from Crossref.

    Args:
        doi (str): The DOI to resolve (e.g., "10.1000/xyz123" or "https://doi.org/10.1000/xyz123").

    Returns:
        dict: Dictionary containing DOI metadata or error.
    """
    # Clean DOI - remove URL prefix if present
    clean_doi = doi.replace("https://doi.org/", "").replace("http://doi.org/", "").strip()
    
    result = _make_crossref_request(f"works/{urllib.parse.quote(clean_doi)}")
    
    if not result.get("success", True):
        return result
    
    if "message" not in result:
        return {
            "success": False,
            "error": "Invalid response from Crossref API"
        }
    
    work = result["message"]
    
    # Extract key metadata
    metadata = {
        "success": True,
        "doi": work.get("DOI", clean_doi),
        "title": work.get("title", [""])[0] if work.get("title") else "",
        "container_title": work.get("container-title", [""])[0] if work.get("container-title") else "",
        "publisher": work.get("publisher", ""),
        "type": work.get("type", ""),
        "published": work.get("published", {}),
        "issued": work.get("issued", {}),
        "volume": work.get("volume", ""),
        "issue": work.get("issue", ""),
        "page": work.get("page", ""),
        "article_number": work.get("article-number", ""),
        "issn": work.get("ISSN", []),
        "isbn": work.get("ISBN", []),
        "url": work.get("URL", ""),
        "abstract": work.get("abstract", ""),
        "reference_count": work.get("reference-count", 0),
        "is_referenced_by_count": work.get("is-referenced-by-count", 0),
        "license": work.get("license", []),
        "link": work.get("link", [])
    }
    
    # Extract authors
    authors = []
    if "author" in work:
        for author in work["author"]:
            author_info = {
                "given": author.get("given", ""),
                "family": author.get("family", ""),
                "sequence": author.get("sequence", ""),
                "orcid": author.get("ORCID", "")
            }
            authors.append(author_info)
    metadata["authors"] = authors
    metadata["author_count"] = len(authors)
    
    return metadata


def tool_search_crossref(query: str, rows: int = 10, offset: int = 0) -> dict:
    """
    Searches Crossref for publications matching a query.

    Args:
        query (str): Search query (title, author, keywords, etc.).
        rows (int): Number of results to return (max 1000). Defaults to 10.
        offset (int): Offset for pagination. Defaults to 0.

    Returns:
        dict: Dictionary containing search results or error.
    """
    params = {
        "query": query,
        "rows": str(min(rows, 1000)),
        "offset": str(offset)
    }
    
    result = _make_crossref_request("works", params)
    
    if not result.get("success", True):
        return result
    
    if "message" not in result or "items" not in result["message"]:
        return {
            "success": False,
            "error": "Invalid response from Crossref API"
        }
    
    items = result["message"]["items"]
    total_results = result["message"].get("total-results", 0)
    
    # Simplify results
    simplified_items = []
    for item in items:
        simplified = {
            "doi": item.get("DOI", ""),
            "title": item.get("title", [""])[0] if item.get("title") else "",
            "container_title": item.get("container-title", [""])[0] if item.get("container-title") else "",
            "publisher": item.get("publisher", ""),
            "type": item.get("type", ""),
            "issued": item.get("issued", {}),
            "score": item.get("score", 0)
        }
        
        # Add authors
        authors = []
        if "author" in item:
            for author in item["author"][:3]:  # Limit to first 3 authors
                authors.append(f"{author.get('given', '')} {author.get('family', '')}".strip())
        simplified["authors"] = authors
        
        simplified_items.append(simplified)
    
    return {
        "success": True,
        "query": query,
        "total_results": total_results,
        "returned_results": len(simplified_items),
        "offset": offset,
        "items": simplified_items
    }


def tool_get_citation(doi: str, style: str = "bibtex") -> dict:
    """
    Gets a formatted citation for a DOI.

    Args:
        doi (str): The DOI to get citation for.
        style (str): Citation style. Options: "bibtex", "apa", "mla", "chicago", "harvard". Defaults to "bibtex".

    Returns:
        dict: Dictionary containing formatted citation or error.
    """
    # First resolve the DOI
    metadata = tool_resolve_doi(doi)
    
    if not metadata.get("success"):
        return metadata
    
    # Format based on style
    if style.lower() == "bibtex":
        citation = _format_bibtex(metadata)
    elif style.lower() == "apa":
        citation = _format_apa(metadata)
    elif style.lower() == "mla":
        citation = _format_mla(metadata)
    elif style.lower() == "chicago":
        citation = _format_chicago(metadata)
    elif style.lower() == "harvard":
        citation = _format_harvard(metadata)
    else:
        return {
            "success": False,
            "error": f"Unsupported citation style: {style}. Use bibtex, apa, mla, chicago, or harvard."
        }
    
    return {
        "success": True,
        "doi": metadata["doi"],
        "style": style,
        "citation": citation
    }


def _format_bibtex(metadata: Dict[str, Any]) -> str:
    """Formats metadata as BibTeX entry."""
    entry_type = metadata.get("type", "article").lower()
    if entry_type == "journal-article":
        entry_type = "article"
    elif entry_type == "proceedings-article":
        entry_type = "inproceedings"
    elif entry_type == "book-chapter":
        entry_type = "incollection"
    
    # Generate citation key
    first_author = metadata.get("authors", [{}])[0].get("family", "Unknown")
    year = metadata.get("issued", {}).get("date-parts", [[""]])[0][0]
    key = f"{first_author}{year}"
    
    lines = [f"@{entry_type}{{{key},"]
    
    # Add fields
    if metadata.get("title"):
        lines.append(f"  title = {{{metadata['title']}}},")
    
    if metadata.get("authors"):
        author_str = " and ".join([
            f"{a.get('family', '')}, {a.get('given', '')}" 
            for a in metadata["authors"]
        ])
        lines.append(f"  author = {{{author_str}}},")
    
    if metadata.get("container_title"):
        lines.append(f"  journal = {{{metadata['container_title']}}},")
    
    if year:
        lines.append(f"  year = {{{year}}},")
    
    if metadata.get("volume"):
        lines.append(f"  volume = {{{metadata['volume']}}},")
    
    if metadata.get("issue"):
        lines.append(f"  number = {{{metadata['issue']}}},")
    
    if metadata.get("page"):
        lines.append(f"  pages = {{{metadata['page']}}},")
    
    if metadata.get("publisher"):
        lines.append(f"  publisher = {{{metadata['publisher']}}},")
    
    if metadata.get("doi"):
        lines.append(f"  doi = {{{metadata['doi']}}},")
    
    if metadata.get("url"):
        lines.append(f"  url = {{{metadata['url']}}},")
    
    lines.append("}")
    
    return "\n".join(lines)


def _format_apa(metadata: Dict[str, Any]) -> str:
    """Formats metadata as APA citation."""
    authors = metadata.get("authors", [])
    year = metadata.get("issued", {}).get("date-parts", [[""]])[0][0]
    title = metadata.get("title", "")
    container = metadata.get("container_title", "")
    volume = metadata.get("volume", "")
    issue = metadata.get("issue", "")
    pages = metadata.get("page", "")
    doi = metadata.get("doi", "")
    
    # Format authors
    if len(authors) == 0:
        author_str = ""
    elif len(authors) == 1:
        author_str = f"{authors[0].get('family', '')}, {authors[0].get('given', '')[0]}."
    elif len(authors) == 2:
        author_str = f"{authors[0].get('family', '')}, {authors[0].get('given', '')[0]}., & {authors[1].get('family', '')}, {authors[1].get('given', '')[0]}."
    else:
        author_str = f"{authors[0].get('family', '')}, {authors[0].get('given', '')[0]}., et al."
    
    citation = f"{author_str} ({year}). {title}."
    
    if container:
        citation += f" *{container}*"
        if volume:
            citation += f", *{volume}*"
            if issue:
                citation += f"({issue})"
        if pages:
            citation += f", {pages}"
    
    citation += "."
    
    if doi:
        citation += f" https://doi.org/{doi}"
    
    return citation


def _format_mla(metadata: Dict[str, Any]) -> str:
    """Formats metadata as MLA citation."""
    authors = metadata.get("authors", [])
    title = metadata.get("title", "")
    container = metadata.get("container_title", "")
    volume = metadata.get("volume", "")
    issue = metadata.get("issue", "")
    year = metadata.get("issued", {}).get("date-parts", [[""]])[0][0]
    pages = metadata.get("page", "")
    
    # Format authors
    if len(authors) == 0:
        author_str = ""
    elif len(authors) == 1:
        author_str = f"{authors[0].get('family', '')}, {authors[0].get('given', '')}."
    elif len(authors) == 2:
        author_str = f"{authors[0].get('family', '')}, {authors[0].get('given', '')}, and {authors[1].get('given', '')} {authors[1].get('family', '')}."
    else:
        author_str = f"{authors[0].get('family', '')}, {authors[0].get('given', '')}, et al."
    
    citation = f"{author_str} \"{title}.\""
    
    if container:
        citation += f" *{container}*"
        if volume:
            citation += f", vol. {volume}"
            if issue:
                citation += f", no. {issue}"
        if year:
            citation += f", {year}"
        if pages:
            citation += f", pp. {pages}"
    
    citation += "."
    
    return citation


def _format_chicago(metadata: Dict[str, Any]) -> str:
    """Formats metadata as Chicago citation."""
    authors = metadata.get("authors", [])
    title = metadata.get("title", "")
    container = metadata.get("container_title", "")
    volume = metadata.get("volume", "")
    issue = metadata.get("issue", "")
    year = metadata.get("issued", {}).get("date-parts", [[""]])[0][0]
    pages = metadata.get("page", "")
    
    # Format authors
    if len(authors) == 0:
        author_str = ""
    elif len(authors) == 1:
        author_str = f"{authors[0].get('family', '')}, {authors[0].get('given', '')}."
    else:
        author_list = [f"{a.get('given', '')} {a.get('family', '')}" for a in authors[:-1]]
        author_str = ", ".join(author_list) + f", and {authors[-1].get('given', '')} {authors[-1].get('family', '')}."
    
    citation = f"{author_str} \"{title}.\""
    
    if container:
        citation += f" *{container}*"
        if volume:
            citation += f" {volume}"
            if issue:
                citation += f", no. {issue}"
        if year:
            citation += f" ({year})"
        if pages:
            citation += f": {pages}"
    
    citation += "."
    
    return citation


def _format_harvard(metadata: Dict[str, Any]) -> str:
    """Formats metadata as Harvard citation."""
    authors = metadata.get("authors", [])
    year = metadata.get("issued", {}).get("date-parts", [[""]])[0][0]
    title = metadata.get("title", "")
    container = metadata.get("container_title", "")
    volume = metadata.get("volume", "")
    issue = metadata.get("issue", "")
    pages = metadata.get("page", "")
    
    # Format authors
    if len(authors) == 0:
        author_str = ""
    elif len(authors) == 1:
        author_str = f"{authors[0].get('family', '')}, {authors[0].get('given', '')[0]}."
    else:
        author_list = [f"{a.get('family', '')}, {a.get('given', '')[0]}." for a in authors[:-1]]
        author_str = ", ".join(author_list) + f" and {authors[-1].get('family', '')}, {authors[-1].get('given', '')[0]}."
    
    citation = f"{author_str} ({year}) '{title}',"
    
    if container:
        citation += f" *{container}*"
        if volume:
            citation += f", vol. {volume}"
            if issue:
                citation += f", no. {issue}"
        if pages:
            citation += f", pp. {pages}"
    
    citation += "."
    
    return citation


def tool_validate_doi(doi: str) -> dict:
    """
    Validates if a DOI exists and is properly formatted.

    Args:
        doi (str): The DOI to validate.

    Returns:
        dict: Dictionary containing validation result.
    """
    # Clean DOI
    clean_doi = doi.replace("https://doi.org/", "").replace("http://doi.org/", "").strip()
    
    # Check format
    import re
    doi_pattern = r'^10\.\d{4,}/[^\s]+$'
    
    if not re.match(doi_pattern, clean_doi):
        return {
            "success": False,
            "valid": False,
            "error": "Invalid DOI format. DOI should start with '10.' followed by registrant code and suffix."
        }
    
    # Try to resolve
    result = tool_resolve_doi(clean_doi)
    
    if result.get("success"):
        return {
            "success": True,
            "valid": True,
            "doi": clean_doi,
            "title": result.get("title", ""),
            "message": "DOI is valid and resolvable."
        }
    else:
        return {
            "success": True,
            "valid": False,
            "doi": clean_doi,
            "error": result.get("error", "DOI could not be resolved.")
        }


def tool_batch_resolve_dois(dois: List[str]) -> dict:
    """
    Resolves multiple DOIs in batch.

    Args:
        dois (List[str]): List of DOIs to resolve.

    Returns:
        dict: Dictionary containing results for each DOI.
    """
    results = []
    successful = 0
    failed = 0
    
    for doi in dois:
        result = tool_resolve_doi(doi)
        results.append({
            "doi": doi,
            "success": result.get("success", False),
            "title": result.get("title", "") if result.get("success") else None,
            "error": result.get("error") if not result.get("success") else None
        })
        
        if result.get("success"):
            successful += 1
        else:
            failed += 1
    
    return {
        "success": True,
        "total": len(dois),
        "successful": successful,
        "failed": failed,
        "results": results
    }