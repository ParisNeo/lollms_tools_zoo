# Bibliography & Research Tools

A comprehensive collection of tools for academic research, bibliography management, and scholarly communication. This toolset provides integrations with major academic databases and reference management systems.

## Overview

The Bibliography Tools enable automated literature discovery, citation management, and reference organization. Whether you're conducting a systematic review, managing a research library, or generating citations for publications, these tools streamline your academic workflow.

## Sub-Toolsets

| Toolset | Description | API Key Required |
|---------|-------------|------------------|
| [arXiv Tools](arxiv/README.md) | Search, download, and organize papers from arXiv.org | No |
| [DOI Tools](doi/README.md) | Resolve DOIs, fetch Crossref metadata, generate citations | Optional |
| [Zotero Tools](zotero/README.md) | Integrate with Zotero reference manager (local & remote) | Yes (remote only) |

## Quick Start

### 1. Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Or install individual toolset dependencies:

```bash
# For arXiv tools
pip install arxiv requests

# For DOI tools
pip install requests habanero

# For Zotero tools
pip install pyzotero requests
```

### 2. Configuration

Copy the example environment file and configure your API keys:

```bash
cp .env.example .env
```

Edit `.env` with your actual API keys and preferences. See the [Configuration](#configuration) section below for details.

### 3. Basic Usage

```python
# Search arXiv for papers
from arxiv.arxiv_tools import search_arxiv
papers = search_arxiv("machine learning", max_results=5)

# Resolve a DOI
from doi.doi_tools import resolve_doi
metadata = resolve_doi("10.1038/nature12373")

# Search Zotero library
from zotero.zotero_tools import ZoteroRemote
zotero = ZoteroRemote(api_key="...", user_id="...")
items = zotero.search("neural networks")
```

## Configuration

### Environment Variables

Create a `.env` file in this directory with your API credentials. See `.env.example` for a complete template.

#### Required for Zotero Remote Access

| Variable | Description | How to Obtain |
|----------|-------------|---------------|
| `ZOTERO_API_KEY` | Your Zotero API key | https://www.zotero.org/settings/keys |
| `ZOTERO_USER_ID` | Your Zotero user ID | Displayed on API keys page |
| `ZOTERO_LIBRARY_TYPE` | `user` or `group` | Your preference |
| `ZOTERO_GROUP_ID` | Group ID (if using group library) | From group URL |

#### Optional for Enhanced Features

| Variable | Description | Service |
|----------|-------------|---------|
| `CROSSREF_API_KEY` | Higher rate limits | Crossref |
| `CROSSREF_MAILTO` | Your email for polite pool | Crossref |
| `SEMANTIC_SCHOLAR_API_KEY` | Higher rate limits | Semantic Scholar |
| `OPENALEX_MAILTO` | Your email for polite pool | OpenAlex |
| `PUBMED_API_KEY` | NCBI E-utilities access | PubMed |
| `PUBMED_EMAIL` | Your email | PubMed |

#### General Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `BIBLIOGRAPHY_DOWNLOAD_DIR` | `./downloads` | Default download directory |
| `BIBLIOGRAPHY_DEFAULT_CITATION_FORMAT` | `bibtex` | Default citation format |
| `BIBLIOGRAPHY_REQUEST_TIMEOUT` | `30` | Request timeout in seconds |
| `BIBLIOGRAPHY_DEBUG` | `false` | Enable debug logging |

### Example .env File

```env
# Zotero (required for remote access)
ZOTERO_API_KEY=abc123def456ghi789
ZOTERO_USER_ID=12345678
ZOTERO_LIBRARY_TYPE=user

# Crossref (optional)
CROSSREF_MAILTO=researcher@university.edu

# General
BIBLIOGRAPHY_DOWNLOAD_DIR=./papers
BIBLIOGRAPHY_DEFAULT_CITATION_FORMAT=bibtex
```

## Features by Toolset

### arXiv Tools

- **Free & Open**: No API key required
- **Comprehensive Search**: Query by keywords, authors, categories, dates
- **PDF Download**: Retrieve full-text papers
- **Metadata Extraction**: Title, authors, abstract, categories, dates
- **Category Browsing**: Explore by arXiv subject categories

[Full arXiv Documentation →](arxiv/README.md)

### DOI Tools

- **DOI Resolution**: Get metadata from any DOI
- **Crossref Search**: Search millions of publications
- **Citation Generation**: BibTeX, APA, MLA, Chicago, Harvard
- **DOI Validation**: Verify DOI authenticity
- **Batch Processing**: Handle multiple DOIs efficiently

[Full DOI Documentation →](doi/README.md)

### Zotero Tools

- **Dual Mode**: Local database or remote Web API
- **Full CRUD**: Create, read, update, delete references
- **Collection Management**: Organize your library
- **File Attachments**: Download PDFs and files
- **Citation Export**: Multiple formats supported
- **Group Libraries**: Collaborate with teams

[Full Zotero Documentation →](zotero/README.md)

## Common Workflows

### Literature Review

```python
# 1. Search arXiv for recent papers
from arxiv.arxiv_tools import search_arxiv
papers = search_arxiv("transformer models", max_results=20)

# 2. Download interesting papers
from arxiv.arxiv_tools import download_arxiv_paper
for paper in papers[:5]:
    download_arxiv_paper(paper['arxiv_id'], "./review_papers")

# 3. Add to Zotero for organization
from zotero.zotero_tools import ZoteroRemote
zotero = ZoteroRemote(api_key="...", user_id="...")
for paper in papers:
    zotero.create_item({
        "itemType": "preprint",
        "title": paper['title'],
        "creators": [{"creatorType": "author", "name": a} for a in paper['authors']],
        "url": paper['url']
    })
```

### Citation Generation

```python
# Generate citations from DOIs
from doi.doi_tools import generate_citation, batch_resolve_dois

dois = ["10.1038/nature12373", "10.1126/science.1234567"]
metadata_list = batch_resolve_dois(dois)

for doi, metadata in metadata_list.items():
    bibtex = generate_citation(doi, format="bibtex")
    print(bibtex)
```

### Reference Management

```python
# Sync arXiv papers to Zotero
from arxiv.arxiv_tools import get_arxiv_metadata
from zotero.zotero_tools import ZoteroRemote

zotero = ZoteroRemote(api_key="...", user_id="...")

arxiv_ids = ["2301.00001", "2301.00002", "2301.00003"]
for arxiv_id in arxiv_ids:
    metadata = get_arxiv_metadata(arxiv_id)
    zotero.create_item({
        "itemType": "preprint",
        "title": metadata['title'],
        "creators": [{"creatorType": "author", "name": a} for a in metadata['authors']],
        "date": metadata['published'],
        "url": f"https://arxiv.org/abs/{arxiv_id}",
        "extra": f"arXiv:{arxiv_id}"
    })
```

## Rate Limits

| Service | Rate Limit | Notes |
|---------|------------|-------|
| arXiv | 1 request / 3 seconds | Automatic throttling included |
| Crossref (no key) | 50 req/sec (shared) | Use `CROSSREF_MAILTO` for better service |
| Crossref (with key) | Varies | Based on your agreement |
| Zotero Web API | 100 req / 10 sec | Per API key |
| Zotero Local | Unlimited | Local database access |

## Error Handling

All tools include robust error handling:

- **Network failures**: Automatic retry with exponential backoff
- **Rate limiting**: Built-in delays and retry logic
- **Invalid inputs**: Clear error messages with suggestions
- **Missing credentials**: Graceful degradation to free tiers
- **API errors**: Detailed error reporting

## Integration with Lollms

This toolset follows the Lollms Communication Protocol (LCP) standards:

```python
def init_tools_library():
    """Initialize the bibliography tools library."""
    # Lazy initialization - heavy imports happen here
    import arxiv
    import requests
    from pyzotero import zotero
    from habanero import Crossref
    return True
```

### Key LCP Features

- **Lazy Loading**: Dependencies loaded only when tools are first invoked
- **Health Gates**: Failed initialization returns clear error to LLM
- **Module Caching**: Validated modules cached for performance
- **AST Discovery**: Tools discovered without importing modules

## Security Best Practices

1. **Never commit `.env`**: The `.env` file is in `.gitignore`
2. **Use environment variables**: Never hardcode API keys
3. **Rotate keys regularly**: Update API keys periodically
4. **Limit permissions**: Only grant necessary API permissions
5. **Secure storage**: Use secure vaults for production deployments

## Troubleshooting

### Common Issues

**"API key invalid"**
- Verify your API key is correct
- Check that the key has necessary permissions
- Ensure no extra whitespace in `.env` file

**"Rate limit exceeded"**
- Add delays between requests
- Register for API keys for higher limits
- Use batch operations where possible

**"Module not found"**
- Install required dependencies: `pip install -r requirements.txt`
- Check that `init_tools_library()` is properly defined

**"Database locked" (Zotero Local)**
- Close Zotero application
- Wait a few seconds and retry
- Check file permissions

## Contributing

To add new bibliography tools:

1. Create a new subfolder for the toolset
2. Include `init_tools_library()` function
3. Add comprehensive README.md
4. Update this main README.md
5. Add configuration to `.env.example` if needed

## License

This toolset is part of the lollms_tools_zoo project. See the main LICENSE file for details.

## References

- [arXiv API](https://arxiv.org/help/api)
- [Crossref REST API](https://www.crossref.org/documentation/retrieve-metadata/rest-api/)
- [Zotero Web API](https://www.zotero.org/support/dev/web_api/v3/start)
- [Semantic Scholar API](https://www.semanticscholar.org/product/api)
- [OpenAlex Documentation](https://docs.openalex.org/)
- [NCBI E-utilities](https://www.ncbi.nlm.nih.gov/books/NBK25501/)