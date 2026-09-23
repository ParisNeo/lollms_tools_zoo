# Web Search & Content Extraction Tools

This directory contains toolsets for searching the web and extracting content from URLs.

## Available Toolsets

### 1. DuckDuckGo Search (`duckduckgo/`)

Free web search using DuckDuckGo - no API key required.

**Tools:**
- `search_web` - Search the web
- `search_news` - Search news articles
- `search_images` - Search for images
- `search_videos` - Search for videos

**Features:**
- No API key required
- Privacy-focused
- Multiple search types
- Regional customization

[📖 Full Documentation](duckduckgo/README.md)

---

### 2. Web Content Extraction (`web_content/`)

Download, read, and analyze content from any URL.

**Tools:**
- `fetch_url` - Download and extract content
- `read_content` - Read with size limits
- `grep_content` - Search within content
- `peek_content` - Preview top/bottom
- `extract_metadata` - Extract page metadata
- `download_file` - Download binary files

**Features:**
- HTML to text conversion
- Multiple content type support
- Metadata extraction
- Regex search with context
- Size limits and timeouts
- Connection pooling

[📖 Full Documentation](web_content/README.md)

---

## Quick Start

### Installation

```bash
# Install all dependencies
pip install duckduckgo-search requests beautifulsoup4 lxml
```

### Basic Workflow

```python
# 1. Search for content
from duckduckgo_search import search_web

results = search_web("python web scraping tutorials")
print(f"Found {results['count']} results")

# 2. Fetch content from first result
from web_content import fetch_url

url = results['results'][0]['url']
content = fetch_url(url, extract_text=True)
print(content['content'])

# 3. Search within the content
from web_content import grep_content

matches = grep_content(url, "BeautifulSoup")
for match in matches['matches']:
    print(f"Line {match['line_number']}: {match['line']}")

# 4. Download files
from web_content import download_file

download_file("https://example.com/paper.pdf", "paper.pdf")
```

## Common Use Cases

### 1. Research Workflow

```python
# Search for academic papers
papers = search_web("machine learning recent advances")

# Read abstracts
for paper in papers['results'][:5]:
    content = fetch_url(paper['url'])
    print(f"Title: {content['metadata']['title']}")
    print(f"Content: {content['content'][:500]}...")
```

### 2. Content Monitoring

```python
# Check for updates on a page
content = fetch_url("https://example.com/news")

# Search for specific keywords
if grep_content("https://example.com/news", "breaking news")['count'] > 0:
    print("Breaking news found!")
```

### 3. Data Collection

```python
# Search for data sources
sources = search_web("COVID-19 data API")

# Download datasets
for source in sources['results']:
    if '.csv' in source['url'] or '.json' in source['url']:
        download_file(source['url'], f"data/{source['title']}.csv")
```

### 4. Content Analysis

```python
# Extract metadata from multiple pages
urls = ["https://example1.com", "https://example2.com"]

for url in urls:
    metadata = extract_metadata(url)
    print(f"Title: {metadata['title']}")
    print(f"Description: {metadata['description']}")
    print(f"Keywords: {metadata['keywords']}")
```

## Tool Combinations

### Search → Fetch → Grep

```python
# Find and extract specific information
results = search_web("python async programming")
url = results['results'][0]['url']

# Get content
content = fetch_url(url)

# Find all mentions of "asyncio"
matches = grep_content(url, "asyncio", context_lines=3)
for match in matches['matches']:
    print(f"Found at line {match['line_number']}:")
    print(match['context_before'])
    print(f">>> {match['line']}")
    print(match['context_after'])
```

### Search → Download → Process

```python
# Find and download papers
papers = search_web("deep learning pdf")

for paper in papers['results']:
    if '.pdf' in paper['url']:
        result = download_file(paper['url'], f"papers/{paper['title']}.pdf")
        if result['status'] == 'success':
            print(f"Downloaded: {result['size']} bytes")
```

## Error Handling

All tools return standardized dictionaries:

```python
# Success
{
    "status": "success",
    "content": "...",
    "metadata": {...}
}

# Error
{
    "error": "Error message",
    "status_code": 404  # if applicable
}
```

## Best Practices

1. **Always check for errors** before processing results
2. **Use size limits** to prevent memory issues
3. **Respect rate limits** - add delays between requests
4. **Cache results** when fetching the same URL multiple times
5. **Handle timeouts** gracefully
6. **Validate URLs** before fetching
7. **Use appropriate tools** - don't download large files with `fetch_url`

## Rate Limiting

### DuckDuckGo
- Free service with rate limits
- Recommended: 1 request per second
- No API key required

### Web Content
- Depends on target website
- Respect robots.txt
- Add delays between requests to same domain
- Use appropriate User-Agent

## Security Considerations

1. **Validate URLs** before fetching
2. **Sanitize content** before displaying
3. **Limit file sizes** when downloading
4. **Check file types** before saving
5. **Use HTTPS** when possible
6. **Respect robots.txt** and terms of service

## Dependencies

```bash
# Required
pip install duckduckgo-search requests beautifulsoup4

# Optional (faster parsing)
pip install lxml
```

## LCP Compliance

All toolsets follow LCP (LollmsCommunicationProtocol) requirements:

- ✅ Lazy initialization with `init_tools_library()`
- ✅ Tool discovery via `__tools__` metadata
- ✅ Standardized return dictionaries
- ✅ Comprehensive error handling
- ✅ Type hints and docstrings
- ✅ No direct database access

## Contributing

When adding new web search or content extraction tools:

1. Follow the existing patterns
2. Implement lazy initialization
3. Add comprehensive error handling
4. Include type hints and docstrings
5. Create detailed README
6. Add `__tools__` metadata
7. Test without network access

## License

See main project LICENSE file.

## Support

For issues or questions:
1. Check the toolset-specific README
2. Review error messages
3. Verify dependencies are installed
4. Check network connectivity
5. Ensure operator authorization for network access (SAFE MODE)