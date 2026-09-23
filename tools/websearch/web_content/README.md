# Web Content Extraction Toolset

Comprehensive tools for downloading, reading, and analyzing web content from URLs.

## Features

- **Fetch URL Content**: Download and extract content from any URL
- **Read Content**: Read full or partial content with line/character limits
- **Grep Content**: Search within content using regular expressions
- **Peek Content**: View top or bottom portions of content
- **Extract Metadata**: Get page title, description, author, and other metadata
- **Download Files**: Download binary files (PDFs, images, etc.)

## Installation

```bash
pip install requests beautifulsoup4 lxml
```

## Tools

### 1. fetch_url

Fetch content from a URL and extract readable text.

```python
fetch_url(
    url="https://example.com/article",
    extract_text=True,
    timeout=30
)
```

**Returns:**
- `url`: Final URL (after redirects)
- `content_type`: MIME type of content
- `text`: Extracted text (if HTML/text)
- `html`: Raw HTML (if HTML)
- `size_bytes`: Content size
- `status_code`: HTTP status code

### 2. read_content

Read content with optional size and line limits.

```python
# Read first 1000 characters
read_content(
    url="https://example.com/article",
    max_chars=1000
)

# Read lines 10-50
read_content(
    url="https://example.com/article",
    start_line=10,
    end_line=50
)
```

**Returns:**
- `content`: Selected content
- `total_lines`: Total number of lines
- `returned_lines`: Number of lines returned
- `truncated`: Whether content was truncated

### 3. grep_content

Search for patterns within content using regex.

```python
grep_content(
    url="https://example.com/article",
    pattern=r"\b(important|critical)\b",
    case_sensitive=False,
    context_lines=2,
    max_matches=50
)
```

**Returns:**
- `matches`: List of matches with context
- `total_matches`: Total number of matches
- Each match includes:
  - `line_number`: Line number (1-indexed)
  - `line`: Matching line
  - `context_before`: Lines before match
  - `context_after`: Lines after match

### 4. peek_content

View top or bottom of content.

```python
# View first 20 lines
peek_content(
    url="https://example.com/article",
    position="top",
    lines=20
)

# View last 20 lines
peek_content(
    url="https://example.com/article",
    position="bottom",
    lines=20
)
```

**Returns:**
- `content`: Selected lines
- `lines_shown`: Number of lines shown
- `total_lines`: Total lines in content
- `start_line`: Starting line number
- `end_line`: Ending line number

### 5. extract_metadata

Extract metadata from web pages.

```python
extract_metadata(url="https://example.com/article")
```

**Returns:**
- `title`: Page title
- `description`: Meta description
- `author`: Author name
- `keywords`: Keywords
- `og_title`: Open Graph title
- `og_description`: Open Graph description
- `og_image`: Open Graph image URL
- `published_date`: Publication date
- `modified_date`: Last modification date

### 6. download_file

Download binary files (PDFs, images, etc.).

```python
# Auto-generate filename
download_file(url="https://example.com/paper.pdf")

# Specify save path
download_file(
    url="https://example.com/paper.pdf",
    save_path="downloads/paper.pdf"
)
```

**Returns:**
- `file_path`: Path to downloaded file
- `size_bytes`: File size in bytes
- `size_mb`: File size in megabytes
- `content_type`: MIME type

## Usage Examples

### Example 1: Read an Article

```python
# Fetch and read article
result = fetch_url("https://example.com/blog-post")
if "text" in result:
    print(result["text"])
```

### Example 2: Search for Keywords

```python
# Find all mentions of "AI" or "machine learning"
result = grep_content(
    url="https://example.com/article",
    pattern=r"\b(AI|artificial intelligence|machine learning)\b",
    case_sensitive=False
)

for match in result["matches"]:
    print(f"Line {match['line_number']}: {match['line']}")
```

### Example 3: Extract Article Metadata

```python
# Get article information
metadata = extract_metadata("https://example.com/article")
print(f"Title: {metadata['title']}")
print(f"Author: {metadata['author']}")
print(f"Published: {metadata['published_date']}")
```

### Example 4: Download and Process PDF

```python
# Download PDF
result = download_file(
    url="https://arxiv.org/pdf/2301.00001.pdf",
    save_path="papers/paper.pdf"
)

if result["status"] == "success":
    print(f"Downloaded {result['size_mb']} MB to {result['file_path']}")
```

### Example 5: Peek at Long Content

```python
# Check beginning of article
top = peek_content(url, position="top", lines=10)
print("First 10 lines:")
print(top["content"])

# Check end of article
bottom = peek_content(url, position="bottom", lines=10)
print("\nLast 10 lines:")
print(bottom["content"])
```

## Content Type Support

### Fully Supported
- **HTML**: Text extraction, metadata, links
- **Plain Text**: Direct reading
- **JSON**: Direct reading

### Partially Supported
- **PDF**: Download only (use external tools for text extraction)
- **Images**: Download only
- **Other Binary**: Download only

## Caching

Downloaded files are cached in `.lollms_code/cache/web_content/` to avoid repeated downloads.

## Error Handling

All tools return dictionaries with either:
- Success: Relevant data keys
- Error: `{"error": "error message"}`

## Rate Limiting

Be respectful of web servers:
- Use appropriate timeouts
- Don't make excessive requests
- Respect robots.txt
- Consider adding delays between requests

## Security Considerations

- Always validate URLs before fetching
- Be cautious with user-provided URLs
- Don't fetch from untrusted sources
- Be aware of potential security risks (XSS, injection, etc.)

## Integration with Search Tools

This toolset complements the DuckDuckGo search tools:

```python
# 1. Search for content
from tools.websearch.duckduckgo import search_web

results = search_web("machine learning tutorials")

# 2. Fetch and read top result
if results["results"]:
    top_url = results["results"][0]["url"]
    content = fetch_url(top_url)
    print(content["text"])
```

## LCP Compliance

- ✅ `init_tools_library()` function implemented
- ✅ `__tools__` metadata list for discovery
- ✅ Lazy initialization with global session
- ✅ Proper error handling
- ✅ Type hints and docstrings
- ✅ Standardized return dictionaries

## Dependencies

- `requests`: HTTP requests
- `beautifulsoup4`: HTML parsing
- `lxml`: XML/HTML parser

## License

Part of the LCP Tools Library.