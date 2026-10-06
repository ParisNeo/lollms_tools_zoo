"""
arXiv Tools for LCP.

Provides tools for searching and downloading papers from arXiv.
arXiv API is free and does not require authentication.

Return convention (applies to every tool in this library):
    Success: {"status": "success", ...payload keys...}
    Failure: {"status": "error", "error": "<actionable message str>"}
The "error" key is present ONLY when status is "error". No tool ever raises.
"""

import re
import urllib.request
import urllib.parse
import urllib.error
import xml.etree.ElementTree as ET
from typing import Optional
from pathlib import Path

# arXiv Atom API endpoints (no authentication required).
_ARXIV_API_URL = "http://export.arxiv.org/api/query"
_ARXIV_PDF_BASE_URL = "https://arxiv.org/pdf/"

# Namespace map for parsing arXiv Atom feeds.
_ATOM_NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "arxiv": "http://arxiv.org/schemas/atom",
}

# Allowed sort keys for tool_search_arxiv.
_VALID_SORT_KEYS = ("relevance", "lastUpdatedDate", "submittedDate")


def _clean_text(value: Optional[str]) -> Optional[str]:
    """Collapses internal whitespace/newlines in feed text, or None if missing."""
    if value is None:
        return None
    return re.sub(r"\s+", " ", value).strip()


def _error(message: str) -> dict:
    """Builds the standard error envelope. Never raises."""
    return {"status": "error", "error": message}


def _parse_arxiv_id(raw_id) -> Optional[str]:
    """
    Normalizes an arXiv ID string to a bare ID (e.g. "2105.02723v1").

    Accepts bare IDs ("2103.12345", "cs/0112017v1") and abs URLs
    ("https://arxiv.org/abs/2103.12345", "arxiv.org/abs/2103.12345v1").
    Returns None if the input is not a string or nothing usable remains.
    """
    if not isinstance(raw_id, str):
        return None
    text = raw_id.strip()
    if not text:
        return None
    # Strip scheme and host if a full URL was passed.
    match = re.search(r"arxiv\.org/abs/(.+)$", text)
    if match:
        text = match.group(1).strip()
    # Tolerate a trailing query string on bare IDs.
    text = text.split("?")[0].strip()
    if not text:
        return None
    return text


def _parse_feed_entries(data: bytes) -> list:
    """Parses arXiv Atom XML bytes into a list of Element objects."""
    root = ET.fromstring(data)
    return root.findall("atom:entry", _ATOM_NS)


def _entry_to_paper_dict(entry) -> dict:
    """Extracts the full paper metadata dict from one Atom <entry> element."""
    entry_id = _clean_text(entry.find("atom:id", _ATOM_NS).text) or ""
    paper = {
        "id": entry_id.split("/abs/")[-1],
        "title": _clean_text(entry.find("atom:title", _ATOM_NS).text) or "",
        "authors": [
            _clean_text(a.find("atom:name", _ATOM_NS).text) or ""
            for a in entry.findall("atom:author", _ATOM_NS)
        ],
        "summary": _clean_text(entry.find("atom:summary", _ATOM_NS).text) or "",
        "published": _clean_text(entry.find("atom:published", _ATOM_NS).text) or "",
        "updated": _clean_text(entry.find("atom:updated", _ATOM_NS).text) or "",
        "pdf_url": entry_id.replace("/abs/", "/pdf/") + ".pdf",
        "arxiv_url": entry_id,
        "categories": [c.get("term") for c in entry.findall("atom:category", _ATOM_NS)],
    }
    return paper


def init_tools_library() -> dict:
    """
    Initialize the arXiv tools library and report readiness.

    Usage:
        Call once before using any tool_ function to confirm the library is
        loaded and to learn its capabilities. No configuration, API key, or
        credentials are required — the arXiv API is public and free. This
        function performs no network activity and stores no state; calling it
        is a readiness check, not a prerequisite for the other tools.

    Returns:
        dict with keys:
            status (str): "success".
            message (str): Human-readable confirmation that the library is ready.
            tools_count (int): Number of tools exposed by this library (4).
            requires_api_key (bool): Always False — the arXiv API needs no key.
    """
    return {
        "status": "success",
        "message": "arXiv tools initialized successfully.",
        "tools_count": 4,
        "requires_api_key": False,
    }


def tool_search_arxiv(query: str, max_results: int = 10, sort_by: str = "relevance") -> dict:
    """
    Search arXiv for papers matching a free-text query.

    Usage:
        Use this tool to discover papers when you have a topic, keyword set, or
        research question (e.g. "vision transformer", "graph neural networks
        protein folding") but do not yet know specific paper IDs or authors.
        Do NOT use this tool to look up one known paper — pass its ID to
        tool_get_arxiv_paper instead. Do NOT use it when you only know the
        author — use tool_search_arxiv_by_author, which sorts that author's
        papers by submission date. To save a found paper locally, pass its
        "id" to tool_download_arxiv_pdf.

    Args:
        query (str): Free-text search terms. Required, non-empty after
            stripping whitespace. Quotes are not needed. Examples:
            "quantum computing", "attention is all you need".
        max_results (int): Maximum number of papers returned. Optional int,
            default 10, allowed range 1..100 inclusive. Booleans are rejected
            even though bool is a subclass of int (True would yield 1 paper).
            Example: 5.
        sort_by (str): Result ordering. Optional str, default "relevance".
            Must be exactly one of "relevance", "lastUpdatedDate",
            "submittedDate" (case-sensitive). Example: "submittedDate".

    Returns:
        dict with keys:
            status (str): "success" or "error".
            query (str): The normalized query actually searched. Present only
                when status is "success".
            results_count (int): Number of papers returned, 0..max_results.
                0 is a success, not an error — the query matched nothing.
                Present only when status is "success".
            papers (list[dict]): One dict per paper, each with keys:
                id (str): Bare arXiv ID, e.g. "2105.02723v1" — pass this to
                    tool_get_arxiv_paper or tool_download_arxiv_pdf.
                title (str): Paper title, newlines collapsed to spaces.
                authors (list[str]): Author names in order.
                summary (str): Abstract text, whitespace-normalized.
                published (str): Submission date, ISO 8601 UTC timestamp.
                updated (str): Latest revision date, ISO 8601 UTC timestamp.
                pdf_url (str): Direct PDF URL on arxiv.org.
                arxiv_url (str): Abstract page URL on arxiv.org.
                categories (list[str]): arXiv category terms, e.g. ["cs.CV"].
                Present only when status is "success".
            error (str): Actionable description of what went wrong and how to
                fix it. Present only when status is "error".
    """
    # ---- Input validation (never raises) ----
    if not isinstance(query, str):
        return _error(
            "Invalid query: expected a non-empty string (e.g. \"quantum computing\"), got %s."
            % type(query).__name__
        )
    query = query.strip()
    if not query:
        return _error(
            "Invalid query: must be a non-empty string. Provide search terms, e.g. \"vision transformer\"."
        )
    if isinstance(max_results, bool) or not isinstance(max_results, int):
        return _error(
            "Invalid max_results: expected an int in 1..100 (e.g. 10), got %s. Booleans are not accepted."
            % type(max_results).__name__
        )
    if not 1 <= max_results <= 100:
        return _error("Invalid max_results: must be an int in 1..100, got %d." % max_results)
    if not isinstance(sort_by, str) or sort_by not in _VALID_SORT_KEYS:
        return _error(
            "Invalid sort_by: must be one of %s, got %r. Use \"relevance\" for topic matching or \"submittedDate\" for newest papers."
            % (", ".join(repr(k) for k in _VALID_SORT_KEYS), sort_by)
        )

    try:
        params = {
            "search_query": "all:%s" % query,
            "start": 0,
            "max_results": max_results,
            "sortBy": sort_by,
            "sortOrder": "descending",
        }
        url = "%s?%s" % (_ARXIV_API_URL, urllib.parse.urlencode(params))
        with urllib.request.urlopen(url, timeout=30) as response:
            data = response.read()

        entries = _parse_feed_entries(data)
        papers = [_entry_to_paper_dict(e) for e in entries]

        return {
            "status": "success",
            "query": query,
            "results_count": len(papers),
            "papers": papers,
        }

    except urllib.error.URLError as e:
        return _error(
            "Could not reach arXiv (network error: %s). Check connectivity and retry; the arXiv API requires no API key." % e
        )
    except ET.ParseError as e:
        return _error(
            "arXiv returned an unreadable response (parse error: %s). Retry; if it persists, the API may be temporarily degraded." % e
        )
    except Exception as e:  # defensive: never leak a traceback to the caller
        return _error(
            "Unexpected error while searching arXiv: %s. Retry with the same arguments; if it persists, inspect the arXiv API status." % e
        )


def tool_get_arxiv_paper(arxiv_id: str) -> dict:
    """
    Fetch full metadata for one arXiv paper by its ID.

    Usage:
        Use this tool when you already know a paper's arXiv ID (bare ID or
        abs URL) and need its authoritative details: title, authors, abstract,
        dates, categories, DOI, and journal reference. Do NOT use this tool to
        discover papers by topic — use tool_search_arxiv. Do NOT use it to
        list an author's papers — use tool_search_arxiv_by_author. Do NOT use
        it to obtain the PDF file itself — use tool_download_arxiv_pdf, which
        saves the file to the workspace (this tool only returns URLs).

    Args:
        arxiv_id (str): The paper's arXiv identifier. Required, non-empty.
            Accepts bare IDs ("2103.12345", "2103.12345v1", "cs/0112017") and
            abstract URLs ("https://arxiv.org/abs/2103.12345" or
            "arxiv.org/abs/2103.12345v1"); surrounding whitespace is stripped.
            Example: "2105.02723v1".

    Returns:
        dict with keys:
            status (str): "success" or "error".
            paper (dict): Full metadata for the paper, with keys:
                id (str): Bare arXiv ID, e.g. "2105.02723v1".
                title (str): Paper title, newlines collapsed to spaces.
                authors (list[str]): Author names in order.
                summary (str): Abstract text, whitespace-normalized.
                published (str): Submission date, ISO 8601 UTC timestamp.
                updated (str): Latest revision date, ISO 8601 UTC timestamp.
                pdf_url (str): Direct PDF URL on arxiv.org.
                arxiv_url (str): Abstract page URL on arxiv.org.
                categories (list[str]): arXiv category terms, e.g. ["cs.CV"].
                doi (str): DOI of the published version. Present only when the
                    arXiv record provides one; absent otherwise.
                journal_ref (str): Journal citation string. Present only when
                    the arXiv record provides one; absent otherwise.
                Present only when status is "success".
            error (str): Actionable description of what went wrong and how to
                fix it. Present only when status is "error".
    """
    # ---- Input validation (never raises) ----
    normalized_id = _parse_arxiv_id(arxiv_id)
    if normalized_id is None:
        return _error(
            "Invalid arxiv_id: expected a non-empty arXiv ID (e.g. \"2103.12345\", \"2103.12345v1\", or \"https://arxiv.org/abs/2103.12345\"), got empty or non-string input."
        )

    try:
        url = "%s?%s" % (_ARXIV_API_URL, urllib.parse.urlencode({"id_list": normalized_id}))
        with urllib.request.urlopen(url, timeout=30) as response:
            data = response.read()

        root = ET.fromstring(data)
        entry = root.find("atom:entry", _ATOM_NS)

        if entry is None:
            return _error(
                "Paper with ID '%s' not found. Check the ID (e.g. '2103.12345') or get it via tool_search_arxiv." % normalized_id
            )

        paper = _entry_to_paper_dict(entry)
        # Attach optional keys only when the record provides them, so absence is meaningful.
        doi_text = _clean_text(entry.find("arxiv:doi", _ATOM_NS).text) if entry.find("arxiv:doi", _ATOM_NS) is not None else None
        if doi_text:
            paper["doi"] = doi_text
        journal_text = _clean_text(entry.find("arxiv:journal_ref", _ATOM_NS).text) if entry.find("arxiv:journal_ref", _ATOM_NS) is not None else None
        if journal_text:
            paper["journal_ref"] = journal_text

        return {
            "status": "success",
            "paper": paper,
        }

    except urllib.error.URLError as e:
        return _error(
            "Could not reach arXiv (network error: %s). Check connectivity and retry; the arXiv API requires no API key." % e
        )
    except ET.ParseError as e:
        return _error(
            "arXiv returned an unreadable response (parse error: %s). Retry; if it persists, the API may be temporarily degraded." % e
        )
    except Exception as e:  # defensive: never leak a traceback to the caller
        return _error(
            "Unexpected error while fetching paper '%s': %s. Retry; if it persists, verify the ID via tool_search_arxiv." % (normalized_id, e)
        )


def tool_download_arxiv_pdf(arxiv_id: str, output_path: Optional[str] = None) -> dict:
    """
    Download a paper's PDF from arXiv into the workspace.

    Usage:
        Use this tool to obtain the actual PDF file of a paper whose arXiv ID
        you already know, saving it under the workspace root for later reading
        or analysis. Do NOT use this tool merely to get metadata or the PDF
        URL — tool_get_arxiv_paper returns those without downloading anything.
        Do NOT use it to find candidate papers — use tool_search_arxiv (by
        topic) or tool_search_arxiv_by_author (by author) first, then pass a
        result's "id" here. SIDE EFFECT: this tool writes a file to disk.

    Args:
        arxiv_id (str): The paper's arXiv identifier. Required, non-empty.
            Accepts bare IDs ("2103.12345", "2103.12345v1", "cs/0112017") and
            abstract URLs ("https://arxiv.org/abs/2103.12345"); whitespace is
            stripped. The ID is sanitized ("/" becomes "_") when building the
            default filename. Example: "2105.02723v1".
        output_path (Optional[str]): Destination path for the PDF, relative to
            the workspace root. Optional, default None (saves as
            "<sanitized_id>.pdf", e.g. "2105.02723v1.pdf"). If provided, must
            be a non-empty str; a missing ".pdf" suffix is appended
            automatically; absolute paths and paths containing ".." segments
            are rejected. Example: "papers/vit.pdf".

    Returns:
        dict with keys:
            status (str): "success" or "error".
            arxiv_id (str): The normalized bare ID that was downloaded.
                Present only when status is "success".
            file_path (str): Path of the saved file, relative to the workspace
                root (never a host-absolute path). Example: "2105.02723v1.pdf".
                Present only when status is "success".
            file_size_bytes (int): Size of the downloaded PDF in bytes.
                Present only when status is "success".
            message (str): Human-readable confirmation including the path.
                Present only when status is "success".
            error (str): Actionable description of what went wrong and how to
                fix it. Present only when status is "error".
    """
    # ---- Input validation (never raises) ----
    normalized_id = _parse_arxiv_id(arxiv_id)
    if normalized_id is None:
        return _error(
            "Invalid arxiv_id: expected a non-empty arXiv ID (e.g. \"2103.12345\" or \"https://arxiv.org/abs/2103.12345\"), got empty or non-string input."
        )

    if output_path is None:
        output_path = "%s.pdf" % normalized_id.replace("/", "_")
    else:
        if not isinstance(output_path, str) or not output_path.strip():
            return _error(
                "Invalid output_path: expected a non-empty path string ending in \".pdf\" relative to the workspace root (e.g. \"papers/vit.pdf\"), or None for the default \"<id>.pdf\"."
            )
        candidate = output_path.strip()
        if Path(candidate).is_absolute():
            return _error(
                "Invalid output_path: absolute paths are rejected. Provide a path relative to the workspace root, e.g. \"papers/vit.pdf\"."
            )
        if ".." in Path(candidate).parts:
            return _error(
                "Invalid output_path: paths must stay inside the workspace (no \"..\" segments). Provide a relative path like \"papers/vit.pdf\"."
            )
        if not candidate.lower().endswith(".pdf"):
            candidate += ".pdf"
        output_path = candidate

    try:
        pdf_url = "%s%s.pdf" % (_ARXIV_PDF_BASE_URL, normalized_id)
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with urllib.request.urlopen(pdf_url, timeout=60) as response:
            pdf_data = response.read()

        output_file.write_bytes(pdf_data)

        return {
            "status": "success",
            "arxiv_id": normalized_id,
            "file_path": output_path,
            "file_size_bytes": len(pdf_data),
            "message": "PDF downloaded successfully to '%s' (relative to the workspace root)." % output_path,
        }

    except urllib.error.HTTPError as e:
        return _error(
            "Could not download PDF for '%s' (HTTP %s). The paper may have no PDF available, or the ID may be wrong; verify with tool_get_arxiv_paper." % (normalized_id, e.code)
        )
    except urllib.error.URLError as e:
        return _error(
            "Could not reach arXiv (network error: %s). Check connectivity and retry; the arXiv API requires no API key." % e
        )
    except OSError as e:
        return _error(
            "Could not write the PDF to '%s' (filesystem error: %s). Choose a different output_path relative to the workspace root." % (output_path, e)
        )
    except Exception as e:  # defensive: never leak a traceback to the caller
        return _error(
            "Unexpected error while downloading PDF for '%s': %s. Retry; if it persists, verify the ID with tool_get_arxiv_paper." % (normalized_id, e)
        )


def tool_search_arxiv_by_author(author_name: str, max_results: int = 10) -> dict:
    """
    Search arXiv for papers by a specific author.

    Usage:
        Use this tool to list a known author's papers, newest first — for
        example to survey someone's recent work or find a specific author's
        publication. Do NOT use this tool for topic-based discovery — use
        tool_search_arxiv, which matches text across the whole record. Do NOT
        use it when you already have a paper ID — use tool_get_arxiv_paper for
        full details of that one paper. To save any returned paper locally,
        pass its "id" to tool_download_arxiv_pdf.

    Args:
        author_name (str): Full or partial author name. Required, non-empty
            after stripping whitespace; quotes are not needed. Matching is
            case-insensitive on the arXiv API side. Examples: "Yann LeCun",
            "Melas-Kyriazi".
        max_results (int): Maximum number of papers returned. Optional int,
            default 10, allowed range 1..100 inclusive; booleans are rejected
            (True would silently mean 1 paper). Example: 5.

    Returns:
        dict with keys:
            status (str): "success" or "error".
            author (str): The normalized author name actually searched.
                Present only when status is "success".
            results_count (int): Number of papers returned, 0..max_results.
                0 is a success, not an error — no author matched, or they
                have no papers in range. Present only when status is "success".
            papers (list[dict]): One dict per paper, each with keys:
                id (str): Bare arXiv ID, e.g. "2610.06805v1" — pass this to
                    tool_get_arxiv_paper or tool_download_arxiv_pdf.
                title (str): Paper title, newlines collapsed to spaces.
                authors (list[str]): All author names of the paper, in order
                    (the searched author is among them).
                published (str): Submission date, ISO 8601 UTC timestamp.
                arxiv_url (str): Abstract page URL on arxiv.org.
                Present only when status is "success".
            error (str): Actionable description of what went wrong and how to
                fix it. Present only when status is "error".
    """
    # ---- Input validation (never raises) ----
    if not isinstance(author_name, str):
        return _error(
            "Invalid author_name: expected a non-empty string (e.g. \"Yann LeCun\"), got %s."
            % type(author_name).__name__
        )
    author_name = author_name.strip()
    if not author_name:
        return _error(
            "Invalid author_name: must be a non-empty string. Provide an author name, e.g. \"Yann LeCun\"."
        )
    if isinstance(max_results, bool) or not isinstance(max_results, int):
        return _error(
            "Invalid max_results: expected an int in 1..100 (e.g. 10), got %s. Booleans are not accepted."
            % type(max_results).__name__
        )
    if not 1 <= max_results <= 100:
        return _error("Invalid max_results: must be an int in 1..100, got %d." % max_results)

    try:
        params = {
            "search_query": "au:\"%s\"" % author_name,
            "start": 0,
            "max_results": max_results,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }
        url = "%s?%s" % (_ARXIV_API_URL, urllib.parse.urlencode(params))
        with urllib.request.urlopen(url, timeout=30) as response:
            data = response.read()

        entries = _parse_feed_entries(data)
        papers = [
            {
                "id": e.find("atom:id", _ATOM_NS).text.split("/abs/")[-1],
                "title": _clean_text(e.find("atom:title", _ATOM_NS).text) or "",
                "authors": [
                    _clean_text(a.find("atom:name", _ATOM_NS).text) or ""
                    for a in e.findall("atom:author", _ATOM_NS)
                ],
                "published": _clean_text(e.find("atom:published", _ATOM_NS).text) or "",
                "arxiv_url": e.find("atom:id", _ATOM_NS).text,
            }
            for e in entries
        ]

        return {
            "status": "success",
            "author": author_name,
            "results_count": len(papers),
            "papers": papers,
        }

    except urllib.error.URLError as e:
        return _error(
            "Could not reach arXiv (network error: %s). Check connectivity and retry; the arXiv API requires no API key." % e
        )
    except ET.ParseError as e:
        return _error(
            "arXiv returned an unreadable response (parse error: %s). Retry; if it persists, the API may be temporarily degraded." % e
        )
    except Exception as e:  # defensive: never leak a traceback to the caller
        return _error(
            "Unexpected error while searching arXiv by author: %s. Retry with the same arguments; if it persists, inspect the arXiv API status." % e
        )
