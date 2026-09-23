# Google Custom Search Toolset

This toolset provides web and image search capabilities using the Google Custom Search API.

## Features

- **Web Search**: Search the web with Google's powerful search engine
- **Image Search**: Find images with advanced filtering options
- **Safe Search**: Configurable content filtering
- **Localization**: Support for multiple languages and regions
- **Rich Metadata**: Detailed search result information

## Setup

### 1. Get Google API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the "Custom Search API"
4. Go to "Credentials" and create an API key
5. Restrict the API key to "Custom Search API" (recommended)

### 2. Create Custom Search Engine

1. Go to [Google Custom Search Engine](https://cse.google.com/)
2. Click "Add" to create a new search engine
3. Configure your search engine:
   - **Sites to search**: Leave empty to search the entire web
   - **Name**: Give your search engine a name
   - **Language**: Select your preferred language
4. Click "Create"
5. Copy the "Search engine ID" from the setup page

### 3. Environment Variables

Create a `.env` file in your project root:

```env
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id_here
```

## Tools

### `google_web_search`

Perform a web search using Google Custom Search API.

**Parameters:**
- `query` (string, required): The search query
- `num_results` (integer, optional): Number of results (1-10, default: 10)
- `start_index` (integer, optional): Starting index for pagination (default: 1)
- `safe_search` (string, optional): Safe search setting ("off", "medium", "high", default: "medium")
- `language` (string, optional): Language code (default: "en")

**Returns:**
```json
{
  "status": "success",
  "data": {
    "query": "search query",
    "total_results": "1000000",
    "search_time": 0.5,
    "formatted_total_results": "1,000,000",
    "formatted_search_time": "0.50",
    "results": [
      {
        "title": "Result Title",
        "url": "https://example.com",
        "snippet": "Result description...",
        "display_url": "example.com",
        "formatted_url": "https://example.com",
        "html_snippet": "<b>Result</b> description...",
        "cache_id": "cache_id",
        "breadcrumb": {}
      }
    ],
    "num_results": 10,
    "start_index": 1,
    "safe_search": "medium",
    "language": "en"
  }
}
```

### `google_image_search`

Perform an image search using Google Custom Search API.

**Parameters:**
- `query` (string, required): The search query
- `num_results` (integer, optional): Number of results (1-10, default: 10)
- `start_index` (integer, optional): Starting index for pagination (default: 1)
- `safe_search` (string, optional): Safe search setting ("off", "medium", "high", default: "medium")
- `image_size` (string, optional): Image size ("small", "medium", "large", "xlarge", "xxlarge", "huge", default: "medium")
- `image_type` (string, optional): Image type ("clipart", "face", "lineart", "news", "photo", default: "photo")

**Returns:**
```json
{
  "status": "success",
  "data": {
    "query": "search query",
    "total_results": "500000",
    "search_time": 0.3,
    "formatted_total_results": "500,000",
    "formatted_search_time": "0.30",
    "results": [
      {
        "title": "Image Title",
        "url": "https://example.com/image.jpg",
        "snippet": "Image description...",
        "display_url": "example.com",
        "image_url": "https://example.com/image.jpg",
        "thumbnail_url": "https://example.com/thumb.jpg",
        "image_width": 800,
        "image_height": 600,
        "image_size": 50000,
        "mime_type": "image/jpeg",
        "file_format": "jpeg"
      }
    ],
    "num_results": 10,
    "start_index": 1,
    "safe_search": "medium",
    "image_size": "medium",
    "image_type": "photo"
  }
}
```

## Usage Examples

### Basic Web Search

```python
# Search for information about Python programming
result = google_web_search("Python programming tutorial", num_results=5)
if result["status"] == "success":
    for item in result["data"]["results"]:
        print(f"Title: {item['title']}")
        print(f"URL: {item['url']}")
        print(f"Snippet: {item['snippet']}")
        print("---")
```

### Image Search

```python
# Search for images of cats
result = google_image_search("cute cats", num_results=8, image_size="large")
if result["status"] == "success":
    for item in result["data"]["results"]:
        print(f"Title: {item['title']}")
        print(f"Image URL: {item['image_url']}")
        print(f"Size: {item['image_width']}x{item['image_height']}")
        print("---")
```

### Advanced Search with Pagination

```python
# Search with pagination
for page in range(1, 4):  # Get first 3 pages
    start_index = (page - 1) * 10 + 1
    result = google_web_search(
        "machine learning", 
        num_results=10, 
        start_index=start_index,
        safe_search="high"
    )
    if result["status"] == "success":
        print(f"Page {page} results:")
        for item in result["data"]["results"]:
            print(f"- {item['title']}")
```

## Rate Limits

- **Free tier**: 100 searches per day
- **Paid tier**: Up to 10,000 searches per day
- **Rate limiting**: Built-in protection against quota exceeded

## Error Handling

The toolset includes comprehensive error handling:

- **API Key Issues**: Clear error messages for missing or invalid API keys
- **Quota Exceeded**: Graceful handling of rate limit exceeded
- **Network Errors**: Timeout and connection error handling
- **Invalid Parameters**: Parameter validation with helpful error messages

## Dependencies

- `requests`: HTTP library for API calls
- `os`: Environment variable access
- `logging`: Error and info logging
- `typing`: Type hints

## LCP Integration

This toolset follows LCP (LollmsCommunicationProtocol) standards:

- **Lazy Initialization**: `init_tools_library()` called on first use
- **Health Gates**: API validation before tool execution
- **Standardized Returns**: Consistent `{"status": "success", "data": {...}}` format
- **Error Handling**: Comprehensive error messages
- **Type Hints**: Full parameter type annotations
- **Documentation**: Google-style docstrings

## Troubleshooting

### Common Issues

1. **"GOOGLE_API_KEY environment variable not set"**
   - Solution: Set the `GOOGLE_API_KEY` environment variable

2. **"GOOGLE_SEARCH_ENGINE_ID environment variable not set"**
   - Solution: Set the `GOOGLE_SEARCH_ENGINE_ID` environment variable

3. **"Quota exceeded"**
   - Solution: Wait for quota reset or upgrade to paid tier

4. **"Invalid API key"**
   - Solution: Check that your API key is correct and has Custom Search API enabled

### Getting Help

- [Google Custom Search API Documentation](https://developers.google.com/custom-search/v1/overview)
- [Google Cloud Console](https://console.cloud.google.com/)
- [Google Custom Search Engine](https://cse.google.com/)