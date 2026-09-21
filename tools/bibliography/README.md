# Bibliography Tools

Comprehensive academic research and bibliography management tools for LCP.

## Overview

This category provides tools for searching, retrieving, and managing academic papers from multiple sources including arXiv, Google Scholar, Semantic Scholar, CrossRef, and Zotero. It supports the full research workflow from discovery to citation management.

## Toolsets

### 📚 [arXiv Tools](arxiv/README.md)
Search and download preprints from arXiv.org

**Key Features:**
- Search 2M+ preprints across physics, math, CS, and more
- Download PDFs and source files
- Get detailed metadata including authors, abstracts, and categories
- Track paper versions and updates

**Use Cases:** Preprint discovery, early access to research, arXiv paper management

---

### 🎓 [Google Scholar Tools](google_scholar/README.md)
Search and analyze papers using Google Scholar

**Key Features:**
- Search Google Scholar's vast database
- Get citation counts and author metrics
- Find papers by author
- Access author profiles with h-index

**Use Cases:** Citation analysis, author metrics, comprehensive literature search

**Note:** No API key required, but has rate limits

---

### 🔬 [Semantic Scholar Tools](semantic_scholar/README.md)
Search and analyze papers using the Semantic Scholar API

**Key Features:**
- Search 200M+ papers with rich metadata
- Explore citation graphs (citations and references)
- Get author details and metrics
- Access abstracts and open access PDFs

**Use Cases:** Citation graph analysis, author impact analysis, research trends

**Note:** Free API with 100 requests per 5 minutes

---

### 📖 [CrossRef Tools](crossref/README.md)
Search and resolve DOIs using the CrossRef API

**Key Features:**
- Search 140M+ academic works
- Resolve DOIs to full metadata
- Search by author, title, journal, or funder
- Get citation counts and references

**Use Cases:** DOI resolution, journal analysis, funding tracking

**Note:** Official DOI registration agency, no API key required

---

### 🔗 [DOI Tools](doi/README.md)
Resolve and validate DOIs

**Key Features:**
- Resolve DOIs to metadata
- Validate DOI format
- Extract DOI from URLs
- Get citation information

**Use Cases:** DOI validation, metadata extraction, citation formatting

---

### 📁 [Zotero Tools](zotero/README.md)
Manage your Zotero library

**Key Features:**
- Search local Zotero database
- Add items to Zotero
- Export citations in multiple formats
- Sync with Zotero cloud (optional)

**Use Cases:** Reference management, citation export, library organization

**Note:** Local mode requires no API key, cloud mode requires Zotero API key

---

## Quick Start

### 1. Search for Papers

```python
# Search arXiv
from arxiv.arxiv_tools import tool_search_arxiv
result = tool_search_arxiv("transformer models", max_results=10)

# Search Google Scholar
from google_scholar.google_scholar_tools import tool_search_google_scholar
result = tool_search_google_scholar("transformer models", num_results=10)

# Search Semantic Scholar
from semantic_scholar.semantic_scholar_tools import tool_search_semantic_scholar
result = tool_search_semantic_scholar("transformer models", num_results=10)

# Search CrossRef
from crossref.crossref_tools import tool_search_crossref
result = tool_search_crossref("transformer models", num_results=10)
```

### 2. Get Paper Details

```python
# By DOI (CrossRef)
from crossref.crossref_tools import tool_get_work_by_doi
result = tool_get_work_by_doi("10.1038/nature14539")

# By DOI (Semantic Scholar)
from semantic_scholar.semantic_scholar_tools import tool_get_paper_details
result = tool_get_paper_details("DOI:10.1038/nature14539")

# By arXiv ID
from arxiv.arxiv_tools import tool_get_arxiv_paper
result = tool_get_arxiv_paper("2106.15928")
```

### 3. Analyze Citations

```python
# Get citations (Semantic Scholar)
from semantic_scholar.semantic_scholar_tools import tool_get_paper_citations
result = tool_get_paper_citations("DOI:10.1038/nature14539", num_results=20)

# Get citation count (Google Scholar)
from google_scholar.google_scholar_tools import tool_get_scholar_citations
result = tool_get_scholar_citations("Attention is all you need", "Vaswani")
```

### 4. Author Analysis

```python
# Search authors (Semantic Scholar)
from semantic_scholar.semantic_scholar_tools import tool_search_authors
result = tool_search_authors("Yann LeCun")

# Get author profile (Google Scholar)
from google_scholar.google_scholar_tools import tool_get_scholar_profile
result = tool_get_scholar_profile("Yann LeCun", "NYU")

# Get author papers (Semantic Scholar)
from semantic_scholar.semantic_scholar_tools import tool_get_author_papers
result = tool_get_author_papers("1741101", num_results=20)
```

## Comparison Matrix

| Feature | arXiv | Google Scholar | Semantic Scholar | CrossRef |
|---------|-------|----------------|------------------|----------|
| **Database Size** | 2M+ | 400M+ | 200M+ | 140M+ |
| **API Key Required** | No | No | No | No |
| **Rate Limit** | 3s delay | Strict | 100/5min | 50/sec |
| **Citation Graph** | No | Limited | Yes | Limited |
| **Author Metrics** | No | Yes | Yes | No |
| **Full Text** | Yes | Sometimes | Sometimes | No |
| **Preprints** | Yes | Yes | Yes | Some |
| **Official API** | Yes | No | Yes | Yes |

## Common Workflows

### Literature Review

1. **Search** multiple sources for comprehensive coverage
2. **Deduplicate** results using DOIs
3. **Filter** by year, venue, or citations
4. **Export** to Zotero for management

```python
# Search multiple sources
arxiv_results = tool_search_arxiv("quantum computing", max_results=20)
s2_results = tool_search_semantic_scholar("quantum computing", num_results=20)
crossref_results = tool_search_crossref("quantum computing", num_results=20)

# Combine and deduplicate by DOI
all_papers = {}
for paper in arxiv_results['papers'] + s2_results['papers'] + crossref_results['works']:
    doi = paper.get('doi') or paper.get('externalIds', {}).get('DOI')
    if doi and doi not in all_papers:
        all_papers[doi] = paper
```

### Citation Analysis

1. **Find** a seminal paper
2. **Get** its citations and references
3. **Analyze** citation network
4. **Identify** influential papers

```python
# Get paper details
paper = tool_get_paper_details("DOI:10.1038/nature14539")

# Get citations
citations = tool_get_paper_citations("DOI:10.1038/nature14539", num_results=100)

# Get references
references = tool_get_paper_references("DOI:10.1038/nature14539", num_results=100)

# Analyze most cited references
ref_citations = [(r['title'], r['citationCount']) for r in references['references']]
ref_citations.sort(key=lambda x: x[1], reverse=True)
```

### Author Impact Analysis

1. **Search** for author
2. **Get** author metrics
3. **Analyze** publication history
4. **Compare** with peers

```python
# Search for author
authors = tool_search_authors("Geoffrey Hinton")
author_id = authors['authors'][0]['authorId']

# Get author details
details = tool_get_author_details(author_id)
print(f"h-index: {details['author']['hIndex']}")
print(f"Citations: {details['author']['citationCount']}")

# Get author papers
papers = tool_get_author_papers(author_id, num_results=100)
```

## Configuration

### Environment Variables

Create a `.env` file in the bibliography directory:

```bash
# Optional: Zotero API (for cloud sync)
ZOTERO_API_KEY=your_api_key_here
ZOTERO_USER_ID=your_user_id_here

# Optional: Email for CrossRef polite pool
CROSSREF_EMAIL=your.email@example.com
```

See [.env.example](.env.example) for a template.

### Rate Limiting

All toolsets include automatic rate limiting:
- **arXiv**: 3 seconds between requests (API requirement)
- **Google Scholar**: 1 second between requests (recommended)
- **Semantic Scholar**: 100ms between requests (100 req/5min)
- **CrossRef**: 50ms between requests (polite pool)

## Best Practices

1. **Use Multiple Sources**: Different databases have different coverage
2. **Deduplicate Results**: Use DOIs to avoid duplicates
3. **Cache Metadata**: DOIs are permanent, cache results
4. **Respect Rate Limits**: Built-in rate limiting helps
5. **Use Official APIs**: Prefer Semantic Scholar and CrossRef over Google Scholar scraping

## Error Handling

All tools return a dictionary with `success` field:

```python
result = tool_search_arxiv("quantum computing")
if result['success']:
    papers = result['papers']
else:
    print(f"Error: {result['error']}")
```

## Dependencies

- `requests` - HTTP library for API calls
- `feedparser` - RSS/Atom feed parsing (arXiv)
- `python-dotenv` - Environment variable management (optional)

## Installation

```bash
pip install requests feedparser python-dotenv
```

## Contributing

To add a new bibliography toolset:

1. Create a new directory under `tools/bibliography/`
2. Implement tools with `tool_` prefix
3. Add `init_tools_library()` function
4. Add `__tools__` metadata list
5. Create comprehensive README.md
6. Update this README with the new toolset

## License

See main project LICENSE file.

## See Also

- [LCP Documentation](../../doc/README.md) - LCP protocol details
- [Math Tools](../math/README.md) - Mathematical calculations
- [Text Processing Tools](../text_processing/README.md) - Text analysis