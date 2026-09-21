# arXiv Tools

A comprehensive toolset for searching, downloading, and organizing academic papers from arXiv.org.

## Overview

The arXiv Tools provide programmatic access to the arXiv repository, enabling automated literature searches, paper downloads, and metadata extraction. arXiv is a free distribution service and open-access archive for scholarly articles in physics, mathematics, computer science, quantitative biology, quantitative finance, statistics, electrical engineering, systems science, and economics.

## Features

- **Search Papers**: Query arXiv by keywords, authors, categories, or date ranges
- **Download PDFs**: Retrieve full-text PDF files of papers
- **Metadata Extraction**: Get detailed information including title, authors, abstract, categories, and publication dates
- **Batch Operations**: Process multiple papers simultaneously
- **Category Browsing**: Explore papers by arXiv subject categories

## Installation

This toolset requires the following Python packages:

```bash
pip install arxiv requests
```

## Configuration

No API key is required for arXiv. The service is free and open to the public.

## Usage Examples

### Basic Search

```python
from arxiv_tools import search_arxiv

# Search for papers about machine learning
results = search_arxiv(
    query="machine learning",
    max_results=10,
    sort_by="relevance"
)

for paper in results:
    print(f"Title: {paper['title']}")
    print(f"Authors: {', '.join(paper['authors'])}")
    print(f"arXiv ID: {paper['arxiv_id']}")
    print("---")
```

### Download a Paper

```python
from arxiv_tools import download_arxiv_paper

# Download a specific paper by arXiv ID
pdf_path = download_arxiv_paper(
    arxiv_id="2301.00001",
    output_dir="./papers"
)
print(f"Downloaded to: {pdf_path}")
```

### Get Paper Metadata

```python
from arxiv_tools import get_arxiv_metadata

metadata = get_arxiv_metadata("2301.00001")
print(f"Title: {metadata['title']}")
print(f"Abstract: {metadata['abstract']}")
print(f"Published: {metadata['published']}")
print(f"Categories: {metadata['categories']}")
```

### Search by Category

```python
from arxiv_tools import search_by_category

# Search in specific categories (e.g., cs.AI for Artificial Intelligence)
results = search_by_category(
    category="cs.AI",
    max_results=20,
    date_from="2024-01-01"
)
```

## API Reference

### `search_arxiv(query, max_results=10, sort_by="relevance", sort_order="descending")`

Search arXiv for papers matching the query.

**Parameters:**
- `query` (str): Search query string
- `max_results` (int): Maximum number of results to return (default: 10)
- `sort_by` (str): Sort criterion - "relevance", "lastUpdatedDate", or "submittedDate"
- `sort_order` (str): Sort order - "ascending" or "descending"

**Returns:** List of dictionaries containing paper metadata

### `download_arxiv_paper(arxiv_id, output_dir="./downloads")`

Download the PDF of a paper from arXiv.

**Parameters:**
- `arxiv_id` (str): The arXiv identifier (e.g., "2301.00001")
- `output_dir` (str): Directory to save the PDF

**Returns:** Path to the downloaded PDF file

### `get_arxiv_metadata(arxiv_id)`

Retrieve detailed metadata for a specific paper.

**Parameters:**
- `arxiv_id` (str): The arXiv identifier

**Returns:** Dictionary containing paper metadata

### `search_by_category(category, max_results=10, date_from=None, date_to=None)`

Search papers within a specific arXiv category.

**Parameters:**
- `category` (str): arXiv category code (e.g., "cs.AI", "physics.optics")
- `max_results` (int): Maximum number of results
- `date_from` (str): Start date filter (YYYY-MM-DD format)
- `date_to` (str): End date filter (YYYY-MM-DD format)

**Returns:** List of dictionaries containing paper metadata

## arXiv Categories

Common arXiv categories include:

| Category | Description |
|----------|-------------|
| cs.AI | Artificial Intelligence |
| cs.CL | Computation and Language |
| cs.CV | Computer Vision and Pattern Recognition |
| cs.LG | Machine Learning |
| math.CO | Combinatorics |
| physics.optics | Optics |
| quant-ph | Quantum Physics |
| stat.ML | Machine Learning (Statistics) |

For a complete list, visit: https://arxiv.org/category_taxonomy

## Rate Limits

arXiv requests a maximum of 1 request per 3 seconds. The tools include built-in rate limiting to comply with arXiv's terms of service.

## Error Handling

The tools handle common errors gracefully:

- **Invalid arXiv ID**: Returns error message with suggestions
- **Network failures**: Automatic retry with exponential backoff
- **PDF not available**: Returns metadata-only response
- **Rate limiting**: Automatic delay between requests

## Integration with Lollms

This toolset is designed to work with the Lollms Communication Protocol (LCP). The `init_tools_library()` function is called lazily on first tool invocation.

```python
def init_tools_library():
    """Initialize the arXiv tools library."""
    # Lazy initialization - heavy imports happen here
    import arxiv
    import requests
    return True
```

## License

This toolset is part of the lollms_tools_zoo project. See the main LICENSE file for details.

## References

- arXiv API Documentation: https://arxiv.org/help/api
- arXiv Category Taxonomy: https://arxiv.org/category_taxonomy
- Python arxiv package: https://pypi.org/project/arxiv/