# CrossRef Tools

Academic work search and DOI resolution using the CrossRef API.

## Overview

CrossRef is the official DOI registration agency for academic publications. This toolset provides access to over 140 million works with comprehensive metadata, including citations, references, and funding information.

## Features

- **Work Search**: Search 140M+ academic works with advanced filters
- **DOI Resolution**: Get detailed metadata for any DOI
- **Author Search**: Find all works by a specific author
- **Journal Search**: Get works from specific journals
- **Funder Search**: Find works by funding agency
- **No API Key**: Free access with polite pool (email in User-Agent)

## Tools

### `search_crossref`

Search CrossRef for academic works.

**Parameters:**
- `query` (str): Search query string
- `num_results` (int, optional): Number of results (max 1000, default: 10)
- `year_from` (int, optional): Filter works from this year onwards
- `year_to` (int, optional): Filter works up to this year
- `work_type` (str, optional): Filter by type (journal-article, book-chapter, etc.)

**Returns:**
```json
{
  "success": true,
  "query": "machine learning",
  "num_results": 10,
  "total_results": 50000,
  "works": [
    {
      "doi": "10.1234/example",
      "title": "Work Title",
      "type": "journal-article",
      "publisher": "Publisher Name",
      "container_title": "Journal Name",
      "authors": ["Author 1", "Author 2"],
      "year": 2023,
      "publication_date": "2023-01-15",
      "citation_count": 150,
      "reference_count": 50,
      "issn": ["1234-5678"],
      "url": "https://doi.org/...",
      "abstract": "...",
      "subjects": ["Computer Science"]
    }
  ]
}
```

**Example:**
```python
result = search_crossref(
    query="deep learning",
    num_results=20,
    year_from=2020,
    work_type="journal-article"
)
```

### `get_work_by_doi`

Get detailed information about a work by its DOI.

**Parameters:**
- `doi` (str): Digital Object Identifier (e.g., "10.1038/nature14539")

**Returns:**
```json
{
  "success": true,
  "doi": "10.1038/nature14539",
  "work": {
    "doi": "10.1038/nature14539",
    "title": "Work Title",
    "type": "journal-article",
    "publisher": "Nature Publishing Group",
    "container_title": "Nature",
    "authors": [...],
    "year": 2015,
    "citation_count": 50000,
    "reference_count": 50,
    "issn": ["0028-0836"],
    "url": "https://doi.org/10.1038/nature14539",
    "abstract": "...",
    "subjects": ["Biology", "Chemistry"]
  }
}
```

**Example:**
```python
result = get_work_by_doi("10.1038/nature14539")
```

### `search_by_author`

Search for works by author name.

**Parameters:**
- `author_name` (str): Author's name (e.g., "Geoffrey Hinton")
- `num_results` (int, optional): Number of results (default: 10)
- `year_from` (int, optional): Filter works from this year onwards
- `year_to` (int, optional): Filter works up to this year

**Returns:**
```json
{
  "success": true,
  "author": "Yann LeCun",
  "num_results": 10,
  "works": [...]
}
```

**Example:**
```python
result = search_by_author(
    author_name="Yoshua Bengio",
    num_results=20,
    year_from=2020
)
```

### `search_by_title`

Search for works by title.

**Parameters:**
- `title` (str): Paper title
- `num_results` (int, optional): Number of results (default: 10)
- `exact_match` (bool, optional): If True, search for exact title match (default: False)

**Returns:**
```json
{
  "success": true,
  "title": "Attention is all you need",
  "exact_match": true,
  "num_results": 1,
  "works": [...]
}
```

**Example:**
```python
result = search_by_title(
    title="Attention is all you need",
    exact_match=True
)
```

### `get_journal_works`

Get works from a specific journal.

**Parameters:**
- `issn` (str): Journal ISSN (e.g., "0028-0836" for Nature)
- `num_results` (int, optional): Number of results (default: 10)
- `year_from` (int, optional): Filter works from this year onwards
- `year_to` (int, optional): Filter works up to this year

**Returns:**
```json
{
  "success": true,
  "issn": "0028-0836",
  "num_results": 10,
  "works": [...]
}
```

**Example:**
```python
result = get_journal_works(
    issn="0028-0836",
    num_results=20,
    year_from=2023
)
```

### `get_funder_works`

Get works by funding agency.

**Parameters:**
- `funder_id` (str): Funder ID (e.g., "100000001" for NSF)
- `num_results` (int, optional): Number of results (default: 10)
- `year_from` (int, optional): Filter works from this year onwards
- `year_to` (int, optional): Filter works up to this year

**Returns:**
```json
{
  "success": true,
  "funder_id": "100000001",
  "num_results": 10,
  "works": [...]
}
```

**Example:**
```python
result = get_funder_works(
    funder_id="100000001",
    num_results=20,
    year_from=2023
)
```

## Work Types

Common work types in CrossRef:
- `journal-article` - Journal articles
- `book-chapter` - Book chapters
- `book` - Books
- `proceedings-article` - Conference papers
- `dissertation` - Theses and dissertations
- `preprint` - Preprints
- `dataset` - Datasets
- `report` - Technical reports

## Rate Limits

**Polite Pool (Recommended):**
- Include email in User-Agent header
- 50 requests per second
- Automatic rate limiting built into the toolset

**Public Pool (No Email):**
- Shared rate limit with all users
- May experience slower response times

## Common ISSNs

- Nature: `0028-0836`
- Science: `0036-8075`
- Cell: `0092-8674`
- PNAS: `0027-8424`
- Physical Review Letters: `0031-9007`

## Common Funder IDs

- NSF (US): `100000001`
- NIH (US): `100000002`
- European Research Council: `100011199`
- Wellcome Trust: `100010269`
- UK Research and Innovation: `100014102`

Find more at: https://api.crossref.org/funders

## Use Cases

1. **DOI Resolution**: Get metadata for any DOI
2. **Literature Search**: Find papers by keywords, authors, or titles
3. **Journal Analysis**: Analyze publications from specific journals
4. **Funding Analysis**: Track research output by funding agency
5. **Citation Tracking**: Get citation counts for works

## Error Handling

All tools return a dictionary with `success` field:
- `success: true` - Operation completed successfully
- `success: false` - Operation failed, check `error` field

**Common Errors:**
- `"Resource not found"` - Invalid DOI
- `"Rate limit exceeded"` - Too many requests
- `"Invalid ISSN"` - Malformed ISSN

## Dependencies

- `requests` - HTTP library for API calls

## Installation

```bash
pip install requests
```

## API Documentation

Full API documentation: https://api.crossref.org/

## Notes

- No API key required
- Polite pool access requires email in User-Agent
- Automatic rate limiting (50ms between requests)
- Comprehensive metadata including citations and references
- Free access to 140M+ works

## Best Practices

1. **Use Polite Pool**: Configure your email in production
2. **Cache Results**: DOIs are permanent, cache metadata
3. **Batch Requests**: Use filters to reduce result sets
4. **Respect Rate Limits**: Built-in rate limiting helps

## See Also

- [Semantic Scholar Tools](../semantic_scholar/README.md) - Citation graphs and author metrics
- [Google Scholar Tools](../google_scholar/README.md) - Web scraping alternative
- [DOI Tools](../doi/README.md) - DOI resolution and metadata
- [arXiv Tools](../arxiv/README.md) - Preprint repository