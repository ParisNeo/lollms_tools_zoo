# Zotero Tools

A comprehensive toolset for integrating with Zotero, the free and open-source reference management software. Supports both local Zotero database access and remote Zotero Web API operations.

## Overview

Zotero Tools provide two modes of operation:

1. **Local Mode**: Direct access to your local Zotero database (no API key required)
2. **Remote Mode**: Access to Zotero Web API for cloud-synced libraries (requires API key)

## Features

### Local Mode (No API Key Required)
- **Read Local Library**: Access your local Zotero database directly
- **Search Items**: Search by title, author, or tags
- **Export Citations**: Generate citations from local items
- **Collection Management**: Browse and organize collections

### Remote Mode (API Key Required)
- **Cloud Sync**: Access your Zotero library from anywhere
- **Create Items**: Add new references to your library
- **Update Items**: Modify existing references
- **Delete Items**: Remove references from your library
- **Group Libraries**: Access shared group libraries
- **File Attachments**: Download attached PDFs and files

## Installation

This toolset requires the following Python packages:

```bash
pip install pyzotero requests
```

## Configuration

### Local Mode Setup

Local mode requires no API key. Simply ensure Zotero is installed and your database is accessible.

### Remote Mode Setup

1. **Get your Zotero API Key**:
   - Go to https://www.zotero.org/settings/keys
   - Click "Create new private key"
   - Give it a description (e.g., "lollms_tools_zoo")
   - Select permissions (read/write as needed)
   - Copy the generated key

2. **Get your User ID**:
   - Your user ID is displayed on the same settings page
   - It's a numeric ID (e.g., 12345678)

3. **Configure Environment Variables**:

Create a `.env` file in the bibliography folder:

```env
# Zotero Remote API Configuration
ZOTERO_API_KEY=your_api_key_here
ZOTERO_USER_ID=your_user_id_here
ZOTERO_LIBRARY_TYPE=user  # or 'group' for group libraries
ZOTERO_GROUP_ID=your_group_id_here  # only if using group library
```

See `.env.example` for a complete configuration template.

## Usage Examples

### Local Mode

```python
from zotero_tools import ZoteroLocal

# Initialize local Zotero connection
zotero = ZoteroLocal()

# Search local library
results = zotero.search("machine learning")
for item in results:
    print(f"Title: {item['title']}")
    print(f"Authors: {item['authors']}")
    print("---")

# Get all items in a collection
collection_items = zotero.get_collection_items("My Collection")
```

### Remote Mode

```python
from zotero_tools import ZoteroRemote

# Initialize remote Zotero connection
zotero = ZoteroRemote(
    api_key="your_api_key",
    user_id="your_user_id",
    library_type="user"
)

# Search remote library
results = zotero.search("neural networks")
for item in results:
    print(f"Title: {item['data']['title']}")
    print(f"Key: {item['key']}")
    print("---")
```

### Create a New Item (Remote Mode)

```python
from zotero_tools import ZoteroRemote

zotero = ZoteroRemote(api_key="...", user_id="...")

# Create a new journal article
new_item = {
    "itemType": "journalArticle",
    "title": "Deep Learning Advances",
    "creators": [
        {"creatorType": "author", "firstName": "John", "lastName": "Doe"},
        {"creatorType": "author", "firstName": "Jane", "lastName": "Smith"}
    ],
    "publicationTitle": "Nature Machine Intelligence",
    "date": "2024",
    "DOI": "10.1038/s42256-024-00001-x"
}

created = zotero.create_item(new_item)
print(f"Created item with key: {created['key']}")
```

### Download Attachment (Remote Mode)

```python
from zotero_tools import ZoteroRemote

zotero = ZoteroRemote(api_key="...", user_id="...")

# Download PDF attachment
attachment_key = "ABC123XYZ"
pdf_path = zotero.download_attachment(
    attachment_key=attachment_key,
    output_dir="./downloads"
)
print(f"Downloaded to: {pdf_path}")
```

### Export Citations

```python
from zotero_tools import export_citations

# Export items to BibTeX
items = zotero.search("quantum computing")
bibtex = export_citations(items, format="bibtex")

with open("references.bib", "w", encoding="utf-8") as f:
    f.write(bibtex)
```

## API Reference

### Local Mode Classes

#### `ZoteroLocal(database_path=None)`

Initialize local Zotero database connection.

**Parameters:**
- `database_path` (str): Path to zotero.sqlite (auto-detected if None)

**Methods:**
- `search(query, item_type=None)`: Search local library
- `get_item(item_key)`: Get specific item by key
- `get_collections()`: List all collections
- `get_collection_items(collection_name)`: Get items in a collection
- `get_tags()`: List all tags

### Remote Mode Classes

#### `ZoteroRemote(api_key, user_id, library_type="user", group_id=None)`

Initialize remote Zotero API connection.

**Parameters:**
- `api_key` (str): Your Zotero API key
- `user_id` (str): Your Zotero user ID
- `library_type` (str): "user" or "group"
- `group_id` (str): Group ID (required if library_type is "group")

**Methods:**
- `search(query, item_type=None, tag=None)`: Search library
- `get_item(item_key)`: Get specific item
- `create_item(item_data)`: Create new item
- `update_item(item_key, item_data)`: Update existing item
- `delete_item(item_key)`: Delete item
- `get_collections()`: List all collections
- `download_attachment(attachment_key, output_dir)`: Download file attachment
- `get_children(item_key)`: Get child items (attachments, notes)

### Utility Functions

#### `export_citations(items, format="bibtex")`

Export items to citation format.

**Parameters:**
- `items` (list): List of Zotero items
- `format` (str): "bibtex", "apa", "mla", "chicago"

**Returns:** Formatted citation string

#### `import_from_doi(doi, zotero_instance)`

Import item from DOI.

**Parameters:**
- `doi` (str): DOI to import
- `zotero_instance`: ZoteroLocal or ZoteroRemote instance

**Returns:** Created/updated item data

## Item Types

Common Zotero item types:

| Type | Description |
|------|-------------|
| journalArticle | Journal article |
| book | Book |
| bookSection | Book chapter |
| conferencePaper | Conference paper |
| thesis | Thesis or dissertation |
| report | Technical report |
| webpage | Web page |
| preprint | Preprint (e.g., arXiv) |

## Rate Limits

- **Zotero Web API**: 100 requests per 10 seconds per API key
- **Local Mode**: No rate limits (local database access)

## Error Handling

The tools handle common errors gracefully:

- **Invalid API key**: Returns authentication error
- **Item not found**: Returns None with error message
- **Network failures**: Automatic retry with exponential backoff
- **Database locked**: Waits and retries for local mode
- **Rate limiting**: Automatic delay between requests

## Integration with Lollms

This toolset is designed to work with the Lollms Communication Protocol (LCP). The `init_tools_library()` function is called lazily on first tool invocation.

```python
def init_tools_library():
    """Initialize the Zotero tools library."""
    # Lazy initialization - heavy imports happen here
    from pyzotero import zotero
    import requests
    return True
```

## Security Notes

- **Never commit your API key** to version control
- Use environment variables or secure vaults for credentials
- The `.env` file is included in `.gitignore` by default
- Rotate API keys periodically for security

## License

This toolset is part of the lollms_tools_zoo project. See the main LICENSE file for details.

## References

- Zotero Web API Documentation: https://www.zotero.org/support/dev/web_api/v3/start
- PyZotero Documentation: https://pyzotero.readthedocs.io/
- Zotero Item Types: https://www.zotero.org/support/dev/web_api/v3/item_types