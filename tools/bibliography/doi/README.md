# DOI Tools

A toolset for resolving DOIs (Digital Object Identifiers), fetching metadata from Crossref, and managing persistent identifiers for academic publications.

## Overview

DOI Tools provide programmatic access to the Crossref API and DOI resolution services. DOIs are persistent identifiers used to uniquely identify academic papers, datasets, and other research outputs. This toolset enables metadata retrieval, citation generation, and DOI validation.

## Features

- **DOI Resolution**: Resolve DOIs to get publication metadata
- **Crossref Search**: Search the Crossref database by title, author, or keywords
- **Metadata Extraction**: Get comprehensive bibliographic data
- **Citation Generation**: Generate citations in multiple formats (BibTeX, APA, MLA, etc.)
- **DOI Validation**: Verify if a DOI is valid and registered
- **Batch Processing**: Process multiple DOIs simultaneously

## Installation

This toolset requires the following Python packages:

```bash
pip install requests habanero
```

## Configuration

Crossref API is free for basic usage. For higher rate limits, you can register for a free API key at https://www.crossref.org/documentation/retrieve-metadata/rest-api/

### Environment Variables

Create a `.env` file in the bibliography folder with the following variables:

```env
# Crossref API (optional - for higher rate limits)
CROSSREF_API_KEY=your_crossref_api_key_here
CROSSREF_MAILTO=your_email@example.com
```

See `.env.example` for a complete configuration template.

## Usage Examples

### Resolve a DOI

```python
from doi_tools import resolve_doi

# Get metadata for a DOI
metadata = resolve_doi("10.1038/nature12373")
print(f"Title: {metadata['title']}")
print(f"Journal: {metadata['container-title']}")
print(f"Year: {metadata['published']['date-parts'][0][0]}")
print(f"DOI: {metadata['DOI']}")
```

### Search Crossref

```python
from doi_tools import search_crossref

# Search for papers by title
results = search_crossref(
    query="machine learning neural networks",
    max_results=10
)

for item in results:
    print(f"Title: {item['title'][0]}")
    print(f"DOI: {item['DOI']}")
    print("---")
```

### Generate Citation

```python
from doi_tools import generate_citation

# Generate BibTeX citation
bibtex = generate_citation("10.1038/nature12373", format="bibtex")
print(bibtex)

# Generate APA citation
apa = generate_citation("10.1038/nature12373", format="apa")
print(apa)
```

### Validate DOI

```python
from doi_tools import validate_doi

# Check if a DOI is valid
is_valid = validate_doi("10.1038/nature12373")
print(f"Valid: {is_valid}")

# Invalid DOI
is_valid = validate_doi("10.9999/invalid")
print(f"Valid: {is_valid}")  # False
```

### Batch DOI Processing

```python
from doi_tools import batch_resolve_dois

dois = [
    "10.1038/nature12373",
    "10.1126/science.1234567",
    "10.1016/j.cell.2023.01.001"
]

results = batch_resolve_dois(dois)
for doi, metadata in results.items():
    if metadata:
        print(f"{doi}: {metadata['title']}")
    else:
        print(f"{doi}: Failed to resolve")
```

## API Reference

### `resolve_doi(doi)`

Resolve a DOI and retrieve publication metadata.

**Parameters:**
- `doi` (str): The DOI to resolve (e.g., "10.1038/nature12373")

**Returns:** Dictionary containing publication metadata or None if not found

### `search_crossref(query, max_results=10, filter_params=None)`

Search the Crossref database.

**Parameters:**
- `query` (str): Search query string
- `max_results` (int): Maximum number of results (default: 10)
- `filter_params` (dict): Additional filters (e.g., {"from-pub-date": "2020-01-01"})

**Returns:** List of dictionaries containing publication metadata

### `generate_citation(doi, format="bibtex")`

Generate a formatted citation for a DOI.

**Parameters:**
- `doi` (str): The DOI to cite
- `format` (str): Citation format - "bibtex", "apa", "mla", "chicago", "harvard"

**Returns:** Formatted citation string

### `validate_doi(doi)`

Validate if a DOI is properly formatted and registered.

**Parameters:**
- `doi` (str): The DOI to validate

**Returns:** Boolean indicating validity

### `batch_resolve_dois(dois, delay=1.0)`

Resolve multiple DOIs with rate limiting.

**Parameters:**
- `dois` (list): List of DOI strings
- `delay` (float): Delay between requests in seconds (default: 1.0)

**Returns:** Dictionary mapping DOIs to their metadata

## Citation Formats

Supported citation formats:

| Format | Description |
|--------|-------------|
| bibtex | BibTeX format for LaTeX documents |
| apa | American Psychological Association style |
| mla | Modern Language Association style |
| chicago | Chicago Manual of Style |
| harvard | Harvard referencing style |

## Rate Limits

- **Without API key**: 50 requests per second (shared pool)
- **With API key**: Higher limits based on your Crossref agreement
- **Recommended**: Use `CROSSREF_MAILTO` to identify your application

## Error Handling

The tools handle common errors gracefully:

- **Invalid DOI format**: Returns validation error with format guidance
- **DOI not found**: Returns None with error message
- **Network failures**: Automatic retry with exponential backoff
- **Rate limiting**: Automatic delay and retry

## Integration with Lollms

This toolset is designed to work with the Lollms Communication Protocol (LCP). The `init_tools_library()` function is called lazily on first tool invocation.

```python
def init_tools_library():
    """Initialize the DOI tools library."""
    # Lazy initialization - heavy imports happen here
    import requests
    from habanero import Crossref
    return True
```

## License

This toolset is part of the lollms_tools_zoo project. See the main LICENSE file for details.

## References

- Crossref REST API: https://www.crossref.org/documentation/retrieve-metadata/rest-api/
- DOI Handbook: https://www.doi.org/hb.html
- Habanero Python package: https://pypi.org/project/habanero/