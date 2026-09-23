# DuckDuckGo Search Toolset

A free, privacy-focused web search toolset that provides text, news, and image search capabilities without requiring API keys.

## Features

- **Free & No API Key**: Completely free to use, no authentication required
- **Privacy-Focused**: No tracking or data collection
- **Multiple Search Types**: Text, news, and image search
- **Rich Results**: Titles, URLs, snippets, sources, dates, and thumbnails
- **Safe Search**: Configurable content filtering
- **Region Support**: Localization options for different regions
- **Rate Limiting**: Built-in protection against abuse

## Installation

```bash
pip install duckduckgo-search
```

## Usage

### Text Search
```python
from tools.websearch.duckduckgo.duckduckgo_search import duckduckgo_text_search

result = duckduckgo_text_search("Python programming", max_results=5)
if result["status"] == "success":
    for item in result["data"]["results"]:
        print(f"Title: {item['title']}")
        print(f"URL: {item['url']}")
        print(f"Snippet: {item['snippet']}")
```

### News Search
```python
from tools.websearch.duckduckgo.duckduckgo_search import duckduckgo_news_search

result = duckduckgo_news_search("artificial intelligence", max_results=3)
if result["status"] == "success":
    for item in result["data"]["results"]:
        print(f"Title: {item['title']}")
        print(f"Source: {item['source']}")
        print(f"Date: {item['date']}")
        print(f"URL: {item['url']}")
```

### Image Search
```python
from tools.websearch.duckduckgo.duckduckgo_search import duckduckgo_image_search

result = duckduckgo_image_search("cute cats", max_results=3)
if result["status"] == "success":
    for item in result["data"]["results"]:
        print(f"Title: {item['title']}")
        print(f"Image URL: {item['image_url']}")
        print(f"Dimensions: {item['width']}x{item['height']}")
        print(f"Source: {item['source']}")
```

## API Reference

### `duckduckgo_text_search(query, max_results=10, region="wt-wt", safesearch="moderate")`

Search DuckDuckGo for text results.

**Parameters:**
- `query` (str): Search query string
- `max_results` (int): Maximum number of results to return (default: 10)
- `region` (str): Region code for localized results (default: "wt-wt")
- `safesearch` (str): Safe search setting - "on", "moderate", or "off" (default: "moderate")

**Returns:**
- Dictionary with search results or error information

### `duckduckgo_news_search(query, max_results=10, region="wt-wt", safesearch="moderate")`

Search DuckDuckGo for news articles.

**Parameters:**
- `query` (str): Search query string
- `max_results` (int): Maximum number of results to return (default: 10)
- `region` (str): Region code for localized results (default: "wt-wt")
- `safesearch` (str): Safe search setting - "on", "moderate", or "off" (default: "moderate")

**Returns:**
- Dictionary with news results or error information

### `duckduckgo_image_search(query, max_results=10, region="wt-wt", safesearch="moderate")`

Search DuckDuckGo for images.

**Parameters:**
- `query` (str): Search query string
- `max_results` (int): Maximum number of results to return (default: 10)
- `region` (str): Region code for localized results (default: "wt-wt")
- `safesearch` (str): Safe search setting - "on", "moderate", or "off" (default: "moderate")

**Returns:**
- Dictionary with image results or error information

## Return Format

All functions return a standardized dictionary:

**Success:**
```json
{
    "status": "success",
    "data": {
        "query": "search query",
        "total_results": 5,
        "results": [
            {
                "title": "Result Title",
                "url": "https://example.com",
                "snippet": "Result description..."
            }
        ]
    }
}
```

**Error:**
```json
{
    "status": "error",
    "message": "Error description"
}
```

## Rate Limiting

DuckDuckGo has built-in rate limiting. If you encounter rate limits:
- Reduce the frequency of requests
- Use smaller `max_results` values
- Implement exponential backoff in your application

## Privacy

DuckDuckGo is privacy-focused:
- No user tracking
- No data collection
- No personalized results
- HTTPS-only connections

## Error Handling

The toolset handles various error conditions:
- Invalid queries
- Network errors
- Rate limiting
- Invalid parameters

All errors are returned as standardized error dictionaries with descriptive messages.

## LCP Compliance

This toolset follows LCP (LollmsCommunicationProtocol) standards:
- Lazy initialization with `init_tools_library()`
- Standardized return formats
- Comprehensive error handling
- Type hints and docstrings
- Metadata for tool discovery