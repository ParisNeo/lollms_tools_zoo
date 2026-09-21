# Semantic Scholar Tools

Academic paper search and analysis using the Semantic Scholar API.

## Overview

This toolset provides access to Semantic Scholar's comprehensive database of over 200 million academic papers. It uses the official API which provides rich metadata, citation graphs, and author metrics without requiring API keys for basic usage.

## Features

- **Paper Search**: Search 200M+ papers with advanced filters
- **Detailed Metadata**: Get comprehensive paper information including abstracts, venues, and external IDs
- **Citation Graph**: Explore papers that cite or are referenced by a given paper
- **Author Analysis**: Get author details, papers, and metrics (h-index, citation count)
- **No API Key**: Free tier with 100 requests per 5 minutes

## Tools

### `search_semantic_scholar`

Search Semantic Scholar for academic papers.

**Parameters:**
- `query` (str): Search query string
- `num_results` (int, optional): Number of results (max 100, default: 10)
- `year_from` (int, optional): Filter papers from this year onwards
- `year_to` (int, optional): Filter papers up to this year
- `fields` (list, optional): Fields to return (default: title, authors, year, citations)

**Returns:**
```json
{
  "success": true,
  "query": "machine learning",
  "num_results": 10,
  "total_results": 50000,
  "papers": [
    {
      "paperId": "...",
      "title": "Paper Title",
      "authors": [{"authorId": "...", "name": "Author Name"}],
      "year": 2023,
      "citationCount": 150,
      "abstract": "...",
      "url": "https://...",
      "externalIds": {"DOI": "...", "ArXiv": "..."}
    }
  ]
}
```

**Example:**
```python
result = search_semantic_scholar(
    query="transformer models",
    num_results=10,
    year_from=2020
)
```

### `get_paper_details`

Get detailed information about a specific paper.

**Parameters:**
- `paper_id` (str): Paper ID (Semantic Scholar ID, DOI, arXiv ID, or URL)
- `fields` (list, optional): Fields to return

**Supported ID Formats:**
- Semantic Scholar ID: `649def34f8be52c8b66281af98ae884c09aef38b`
- DOI: `DOI:10.1038/nature14539`
- arXiv: `ARXIV:2106.15928`
- URL: `URL:https://arxiv.org/abs/2106.15928`

**Returns:**
```json
{
  "success": true,
  "paper_id": "DOI:10.1038/nature14539",
  "paper": {
    "paperId": "...",
    "title": "...",
    "abstract": "...",
    "year": 2015,
    "citationCount": 50000,
    "referenceCount": 50,
    "influentialCitationCount": 5000,
    "authors": [...],
    "venue": "Nature",
    "journal": {...},
    "openAccessPdf": {"url": "..."},
    "fieldsOfStudy": ["Biology", "Chemistry"]
  }
}
```

**Example:**
```python
result = get_paper_details("DOI:10.1038/nature14539")
```

### `get_paper_citations`

Get papers that cite a given paper.

**Parameters:**
- `paper_id` (str): Paper ID
- `num_results` (int, optional): Number of citing papers (max 1000, default: 10)
- `fields` (list, optional): Fields to return

**Returns:**
```json
{
  "success": true,
  "paper_id": "...",
  "num_citations": 10,
  "citations": [
    {
      "paperId": "...",
      "title": "Citing Paper Title",
      "authors": [...],
      "year": 2023,
      "citationCount": 50
    }
  ]
}
```

**Example:**
```python
result = get_paper_citations(
    paper_id="DOI:10.1038/nature14539",
    num_results=20
)
```

### `get_paper_references`

Get papers referenced by a given paper.

**Parameters:**
- `paper_id` (str): Paper ID
- `num_results` (int, optional): Number of referenced papers (max 1000, default: 10)
- `fields` (list, optional): Fields to return

**Returns:**
```json
{
  "success": true,
  "paper_id": "...",
  "num_references": 10,
  "references": [
    {
      "paperId": "...",
      "title": "Referenced Paper Title",
      "authors": [...],
      "year": 2010,
      "citationCount": 1000
    }
  ]
}
```

**Example:**
```python
result = get_paper_references(
    paper_id="DOI:10.1038/nature14539",
    num_results=20
)
```

### `get_author_papers`

Get papers by a specific author.

**Parameters:**
- `author_id` (str): Semantic Scholar Author ID
- `num_results` (int, optional): Number of papers (max 1000, default: 10)
- `fields` (list, optional): Fields to return

**Returns:**
```json
{
  "success": true,
  "author_id": "1741101",
  "num_papers": 10,
  "papers": [...]
}
```

**Example:**
```python
result = get_author_papers(
    author_id="1741101",
    num_results=20
)
```

### `get_author_details`

Get detailed information about an author.

**Parameters:**
- `author_id` (str): Semantic Scholar Author ID
- `fields` (list, optional): Fields to return

**Returns:**
```json
{
  "success": true,
  "author_id": "1741101",
  "author": {
    "authorId": "1741101",
    "name": "Yann LeCun",
    "affiliations": ["NYU", "Facebook AI Research"],
    "homepage": "http://yann.lecun.com",
    "paperCount": 500,
    "citationCount": 200000,
    "hIndex": 150,
    "url": "https://www.semanticscholar.org/author/1741101"
  }
}
```

**Example:**
```python
result = get_author_details("1741101")
```

### `search_authors`

Search for authors by name.

**Parameters:**
- `query` (str): Author name search query
- `num_results` (int, optional): Number of results (max 1000, default: 10)
- `fields` (list, optional): Fields to return

**Returns:**
```json
{
  "success": true,
  "query": "Yann LeCun",
  "num_results": 5,
  "authors": [
    {
      "authorId": "1741101",
      "name": "Yann LeCun",
      "affiliations": ["NYU"],
      "paperCount": 500,
      "citationCount": 200000,
      "hIndex": 150
    }
  ]
}
```

**Example:**
```python
result = search_authors("Geoffrey Hinton", num_results=5)
```

## Rate Limits

**Free Tier (No API Key):**
- 100 requests per 5 minutes
- Automatic rate limiting built into the toolset

**With API Key:**
- 1000 requests per second
- Get API key at: https://www.semanticscholar.org/product/api

## Available Fields

**Paper Fields:**
- `paperId`, `title`, `abstract`, `year`, `authors`, `citationCount`
- `referenceCount`, `influentialCitationCount`, `url`, `externalIds`
- `venue`, `publicationDate`, `journal`, `openAccessPdf`
- `fieldsOfStudy`, `s2FieldsOfStudy`, `publicationTypes`

**Author Fields:**
- `authorId`, `name`, `affiliations`, `homepage`
- `paperCount`, `citationCount`, `hIndex`, `url`

## Use Cases

1. **Literature Review**: Search and analyze papers in your field
2. **Citation Analysis**: Build citation graphs and track influence
3. **Author Metrics**: Analyze author productivity and impact
4. **Trend Analysis**: Track research trends over time
5. **Recommendation**: Find related papers based on citations

## Error Handling

All tools return a dictionary with `success` field:
- `success: true` - Operation completed successfully
- `success: false` - Operation failed, check `error` field

**Common Errors:**
- `"Paper not found"` - Invalid paper ID
- `"Author not found"` - Invalid author ID
- `"Rate limit exceeded"` - Too many requests (wait 5 minutes)

## Dependencies

- `requests` - HTTP library for API calls

## Installation

```bash
pip install requests
```

## API Documentation

Full API documentation: https://api.semanticscholar.org/

## Notes

- No API key required for basic usage
- Automatic rate limiting (100ms between requests)
- Supports multiple ID formats (DOI, arXiv, Semantic Scholar ID)
- Rich metadata including abstracts and citation graphs
- Free tier suitable for most research use cases

## See Also

- [Google Scholar Tools](../google_scholar/README.md) - Web scraping alternative
- [CrossRef Tools](../crossref/README.md) - DOI registration agency
- [arXiv Tools](../arxiv/README.md) - Preprint repository