# Google Scholar Tools

Academic paper search and citation analysis using Google Scholar.

## Overview

This toolset provides access to Google Scholar's vast database of academic papers without requiring API keys. It uses web scraping to extract paper information, citations, and author metrics.

## Features

- **Paper Search**: Search for papers by keywords, with filters for year and sorting options
- **Citation Analysis**: Get citation counts for specific papers
- **Author Search**: Find all papers by a specific author
- **Author Profiles**: Get h-index, i10-index, and total citations for authors

## Tools

### `search_google_scholar`

Search Google Scholar for academic papers.

**Parameters:**
- `query` (str): Search query string
- `num_results` (int, optional): Number of results (max 20, default: 10)
- `year_from` (int, optional): Filter papers from this year onwards
- `year_to` (int, optional): Filter papers up to this year
- `sort_by` (str, optional): Sort order - "relevance" or "date" (default: "relevance")

**Returns:**
```json
{
  "success": true,
  "query": "machine learning",
  "num_results": 10,
  "papers": [
    {
      "title": "Paper Title",
      "authors_venue": "Author Names - Venue, Year",
      "year": "2023",
      "snippet": "Abstract snippet...",
      "citations": 150,
      "pdf_link": "https://...",
      "scholar_link": "https://scholar.google.com/..."
    }
  ]
}
```

**Example:**
```python
result = search_google_scholar(
    query="transformer neural networks",
    num_results=5,
    year_from=2020,
    sort_by="relevance"
)
```

### `get_scholar_citations`

Get citation count for a specific paper.

**Parameters:**
- `title` (str): Paper title
- `author` (str, optional): Author name to narrow search

**Returns:**
```json
{
  "success": true,
  "title": "Attention is all you need",
  "citations": 50000,
  "year": "2017",
  "scholar_link": "https://scholar.google.com/..."
}
```

**Example:**
```python
result = get_scholar_citations(
    title="Attention is all you need",
    author="Vaswani"
)
```

### `search_scholar_by_author`

Search for papers by a specific author.

**Parameters:**
- `author_name` (str): Author's name
- `num_results` (int, optional): Number of results (default: 10)
- `sort_by` (str, optional): Sort order - "citations" or "date" (default: "citations")

**Returns:**
```json
{
  "success": true,
  "author": "Yann LeCun",
  "num_results": 10,
  "papers": [...],
  "sort_by": "citations"
}
```

**Example:**
```python
result = search_scholar_by_author(
    author_name="Geoffrey Hinton",
    num_results=10,
    sort_by="citations"
)
```

### `get_scholar_profile`

Get Google Scholar profile information for an author.

**Parameters:**
- `author_name` (str): Author's full name
- `affiliation` (str, optional): Affiliation to narrow search

**Returns:**
```json
{
  "success": true,
  "author": "Geoffrey Hinton",
  "affiliation": "University of Toronto",
  "h_index": 150,
  "i10_index": 400,
  "total_citations": 500000,
  "profile_url": "https://scholar.google.com/citations?user=..."
}
```

**Example:**
```python
result = get_scholar_profile(
    author_name="Yoshua Bengio",
    affiliation="University of Montreal"
)
```

## Rate Limits

Google Scholar has rate limits to prevent abuse:
- **Recommended**: Max 1 request per second
- **Burst limit**: ~20 requests before temporary block
- **IP blocking**: Excessive requests may result in temporary IP ban

**Best Practices:**
1. Add delays between requests
2. Cache results when possible
3. Use specific queries to reduce result sets
4. Respect robots.txt

## Limitations

- **No official API**: Uses web scraping (may break if Google changes HTML structure)
- **Rate limits**: Strict rate limiting compared to official APIs
- **Result limit**: Maximum 20 results per query
- **No bulk export**: Cannot export large result sets

## Use Cases

1. **Literature Review**: Find relevant papers for research
2. **Citation Tracking**: Monitor citation counts for papers
3. **Author Analysis**: Analyze author productivity and impact
4. **Trend Analysis**: Track research trends over time

## Error Handling

All tools return a dictionary with `success` field:
- `success: true` - Operation completed successfully
- `success: false` - Operation failed, check `error` field

**Common Errors:**
- `"Paper not found"` - No results for the query
- `"Profile not found"` - Author profile not found
- `"Search failed: ..."` - Network or parsing error

## Dependencies

- `requests` - HTTP library for web scraping

## Installation

```bash
pip install requests
```

## Notes

- This toolset does NOT require API keys
- Results are scraped from Google Scholar's HTML
- Use responsibly to avoid IP blocking
- Consider using official APIs (Semantic Scholar, CrossRef) for production use

## See Also

- [Semantic Scholar Tools](../semantic_scholar/README.md) - Official API with no rate limits
- [CrossRef Tools](../crossref/README.md) - DOI registration agency API
- [arXiv Tools](../arxiv/README.md) - Preprint repository