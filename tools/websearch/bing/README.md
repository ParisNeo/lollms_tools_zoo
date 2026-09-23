# Bing Search Toolset

Web search using Microsoft Bing Search API with free tier (1000 transactions/month).

## Features

- **Web Search**: Comprehensive web search results
- **News Search**: Latest news articles with dates
- **Image Search**: High-quality image results
- **Video Search**: Video search with metadata
- **Market Support**: Localized results for different markets
- **Free Tier**: 1000 free transactions per month

## Installation

```bash
pip install requests
```

## Configuration

1. Get a free API key from [Bing Search API](https://www.microsoft.com/en-us/bing/apis/bing-web-search-api)
2. Add to your `.env` file:

```env
BING_SEARCH_API_KEY=your_api_key_here
```

## Tools

### search_web

Search the web using Bing.

**Parameters:**
- `query` (string, required): Search query
- `max_results` (integer, optional): Maximum results (default: 10, max: 50)
- `market` (string, optional): Market code (default: "en-US")

**Returns:**
```json
{
  "results": [
    {
      "title": "Result Title",
      "url": "https://example.com",
      "snippet": "Result description..."
    }
  ],
  "count": 10,
  "query": "search query",
  "provider": "Bing"
}
```

### search_news

Search for news articles.

**Parameters:**
- `query` (string, required): Search query
- `max_results` (integer, optional): Maximum results (default: 10, max: 100)
- `market` (string, optional): Market code (default: "en-US")

**Returns:**
```json
{
  "results": [
    {
      "title": "News Title",
      "url": "https://news.example.com",
      "snippet": "News description...",
      "date": "2024-01-01T00:00:00",
      "source": "News Source"
    }
  ],
  "count": 10,
  "query": "search query",
  "provider": "Bing News"
}
```

### search_images

Search for images.

**Parameters:**
- `query` (string, required): Search query
- `max_results` (integer, optional): Maximum results (default: 10, max: 150)
- `market` (string, optional): Market code (default: "en-US")

**Returns:**
```json
{
  "results": [
    {
      "title": "Image Title",
      "url": "https://example.com/image.jpg",
      "thumbnail": "https://example.com/thumb.jpg",
      "source": "https://example.com/page"
    }
  ],
  "count": 10,
  "query": "search query",
  "provider": "Bing Images"
}
```

### search_videos

Search for videos.

**Parameters:**
- `query` (string, required): Search query
- `max_results` (integer, optional): Maximum results (default: 10, max: 105)
- `market` (string, optional): Market code (default: "en-US")

**Returns:**
```json
{
  "results": [
    {
      "title": "Video Title",
      "url": "https://video.example.com",
      "duration": "PT5M30S",
      "publisher": "Video Publisher"
    }
  ],
  "count": 10,
  "query": "search query",
  "provider": "Bing Videos"
}
```

## Market Codes

Common market codes:
- `en-US`: United States (English)
- `en-GB`: United Kingdom (English)
- `en-CA`: Canada (English)
- `en-AU`: Australia (English)
- `de-DE`: Germany (German)
- `fr-FR`: France (French)
- `es-ES`: Spain (Spanish)
- `it-IT`: Italy (Italian)
- `ja-JP`: Japan (Japanese)
- `zh-CN`: China (Chinese)

## Pricing

- **Free Tier**: 1000 transactions/month
- **Paid Tiers**: Starting at $7 per 1000 transactions
- See [Bing Search API Pricing](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/search-api/) for details

## Usage Examples

### Basic Web Search
```python
result = search_web("Python programming", max_results=5)
for item in result["results"]:
    print(f"{item['title']}: {item['url']}")
```

### News Search
```python
result = search_news("artificial intelligence", max_results=10)
for article in result["results"]:
    print(f"{article['date']} - {article['title']}")
```

### Image Search
```python
result = search_images("cute cats", max_results=20)
for image in result["results"]:
    print(f"{image['title']}: {image['url']}")
```

## Advantages

1. **High Quality**: Microsoft's search technology
2. **Free Tier**: 1000 free transactions/month
3. **Multiple Search Types**: Web, news, images, videos
4. **Market Support**: Localized results
5. **Reliable**: Enterprise-grade API

## Limitations

1. **API Key Required**: Must register for API key
2. **Rate Limits**: Free tier limited to 1000/month
3. **Cost**: Paid tiers can be expensive for high volume
4. **Requires Internet**: API calls require internet connection

## Error Handling

All tools return dictionaries with either:
- Success: `{"results": [...], "count": N, ...}`
- Error: `{"error": "error message"}`

Common errors:
- Missing API key: Set `BING_SEARCH_API_KEY` environment variable
- Rate limit exceeded: Upgrade to paid tier or wait until next month
- Invalid market code: Use valid market code from list above

## LCP Integration

This toolset follows LCP standards:
- ✅ `init_tools_library()` for lazy initialization
- ✅ `__tools__` metadata for discovery
- ✅ Standardized return dictionaries
- ✅ Comprehensive error handling
- ✅ Type hints and docstrings
- ✅ Environment variable configuration

## License

This toolset uses the Bing Search API.
Bing is a trademark of Microsoft Corporation.