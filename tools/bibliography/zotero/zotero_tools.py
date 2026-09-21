"""
Zotero Integration Toolset for LCP.

Provides tools for interacting with Zotero libraries (local and remote).
Requires Zotero API key for remote access.
"""

import os
import json
from typing import Optional, List, Dict
from pathlib import Path


def init_tools_library() -> dict:
    """
    Initializes the Zotero integration toolset.
    
    Validates that required dependencies are available and checks for API configuration.
    
    Returns:
        dict: Status dictionary indicating initialization result.
    """
    try:
        import requests
        requests_available = True
    except ImportError:
        requests_available = False
    
    api_key = os.environ.get("ZOTERO_API_KEY")
    user_id = os.environ.get("ZOTERO_USER_ID")
    
    return {
        "status": "success",
        "message": "Zotero toolset initialized.",
        "requests_available": requests_available,
        "api_key_configured": api_key is not None,
        "user_id_configured": user_id is not None,
        "tools_count": 8
    }


def tool_search_zotero_library(query: str, limit: int = 10) -> dict:
    """
    Searches the user's Zotero library for items matching a query.
    
    Requires ZOTERO_API_KEY and ZOTERO_USER_ID environment variables.

    Args:
        query (str): Search query string.
        limit (int): Maximum number of results to return. Defaults to 10.

    Returns:
        dict: Dictionary containing search results or error message.
    """
    api_key = os.environ.get("ZOTERO_API_KEY")
    user_id = os.environ.get("ZOTERO_USER_ID")
    
    if not api_key or not user_id:
        return {
            "success": False,
            "error": "Zotero API credentials not configured. Set ZOTERO_API_KEY and ZOTERO_USER_ID environment variables."
        }
    
    try:
        import requests
        
        url = f"https://api.zotero.org/users/{user_id}/items"
        headers = {"Zotero-API-Key": api_key}
        params = {
            "q": query,
            "limit": limit,
            "format": "json"
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        
        items = response.json()
        
        results = []
        for item in items:
            data = item.get("data", {})
            results.append({
                "key": item.get("key"),
                "title": data.get("title", "No title"),
                "creators": [
                    f"{c.get('firstName', '')} {c.get('lastName', '')}".strip()
                    for c in data.get("creators", [])
                ],
                "item_type": data.get("itemType"),
                "date": data.get("date"),
                "doi": data.get("DOI"),
                "url": data.get("url")
            })
        
        return {
            "success": True,
            "query": query,
            "count": len(results),
            "results": results
        }
        
    except ImportError:
        return {
            "success": False,
            "error": "requests library not installed. Install with: pip install requests"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error searching Zotero library: {str(e)}"
        }


def tool_get_zotero_item(item_key: str) -> dict:
    """
    Retrieves detailed information about a specific Zotero item.
    
    Requires ZOTERO_API_KEY and ZOTERO_USER_ID environment variables.

    Args:
        item_key (str): The Zotero item key.

    Returns:
        dict: Dictionary containing item details or error message.
    """
    api_key = os.environ.get("ZOTERO_API_KEY")
    user_id = os.environ.get("ZOTERO_USER_ID")
    
    if not api_key or not user_id:
        return {
            "success": False,
            "error": "Zotero API credentials not configured."
        }
    
    try:
        import requests
        
        url = f"https://api.zotero.org/users/{user_id}/items/{item_key}"
        headers = {"Zotero-API-Key": api_key}
        
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        item = response.json()
        data = item.get("data", {})
        
        return {
            "success": True,
            "key": item.get("key"),
            "version": item.get("version"),
            "title": data.get("title"),
            "creators": data.get("creators", []),
            "item_type": data.get("itemType"),
            "publication": data.get("publicationTitle"),
            "date": data.get("date"),
            "doi": data.get("DOI"),
            "isbn": data.get("ISBN"),
            "abstract": data.get("abstractNote"),
            "url": data.get("url"),
            "tags": [tag.get("tag") for tag in data.get("tags", [])],
            "full_data": data
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Error retrieving Zotero item: {str(e)}"
        }


def tool_list_zotero_collections() -> dict:
    """
    Lists all collections in the user's Zotero library.
    
    Requires ZOTERO_API_KEY and ZOTERO_USER_ID environment variables.

    Returns:
        dict: Dictionary containing list of collections or error message.
    """
    api_key = os.environ.get("ZOTERO_API_KEY")
    user_id = os.environ.get("ZOTERO_USER_ID")
    
    if not api_key or not user_id:
        return {
            "success": False,
            "error": "Zotero API credentials not configured."
        }
    
    try:
        import requests
        
        url = f"https://api.zotero.org/users/{user_id}/collections"
        headers = {"Zotero-API-Key": api_key}
        
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        collections = response.json()
        
        results = []
        for coll in collections:
            data = coll.get("data", {})
            results.append({
                "key": coll.get("key"),
                "name": data.get("name"),
                "parent_collection": data.get("parentCollection"),
                "num_items": coll.get("meta", {}).get("numItems", 0)
            })
        
        return {
            "success": True,
            "count": len(results),
            "collections": results
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Error listing Zotero collections: {str(e)}"
        }


def tool_get_collection_items(collection_key: str, limit: int = 50) -> dict:
    """
    Retrieves items from a specific Zotero collection.
    
    Requires ZOTERO_API_KEY and ZOTERO_USER_ID environment variables.

    Args:
        collection_key (str): The collection key.
        limit (int): Maximum number of items to return. Defaults to 50.

    Returns:
        dict: Dictionary containing collection items or error message.
    """
    api_key = os.environ.get("ZOTERO_API_KEY")
    user_id = os.environ.get("ZOTERO_USER_ID")
    
    if not api_key or not user_id:
        return {
            "success": False,
            "error": "Zotero API credentials not configured."
        }
    
    try:
        import requests
        
        url = f"https://api.zotero.org/users/{user_id}/collections/{collection_key}/items"
        headers = {"Zotero-API-Key": api_key}
        params = {"limit": limit, "format": "json"}
        
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        
        items = response.json()
        
        results = []
        for item in items:
            data = item.get("data", {})
            results.append({
                "key": item.get("key"),
                "title": data.get("title", "No title"),
                "creators": [
                    f"{c.get('firstName', '')} {c.get('lastName', '')}".strip()
                    for c in data.get("creators", [])
                ],
                "item_type": data.get("itemType"),
                "date": data.get("date")
            })
        
        return {
            "success": True,
            "collection_key": collection_key,
            "count": len(results),
            "items": results
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Error retrieving collection items: {str(e)}"
        }


def tool_export_zotero_item_bibtex(item_key: str) -> dict:
    """
    Exports a Zotero item to BibTeX format.
    
    Requires ZOTERO_API_KEY and ZOTERO_USER_ID environment variables.

    Args:
        item_key (str): The Zotero item key.

    Returns:
        dict: Dictionary containing BibTeX entry or error message.
    """
    api_key = os.environ.get("ZOTERO_API_KEY")
    user_id = os.environ.get("ZOTERO_USER_ID")
    
    if not api_key or not user_id:
        return {
            "success": False,
            "error": "Zotero API credentials not configured."
        }
    
    try:
        import requests
        
        url = f"https://api.zotero.org/users/{user_id}/items/{item_key}"
        headers = {"Zotero-API-Key": api_key}
        params = {"format": "bibtex"}
        
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        
        bibtex = response.text
        
        return {
            "success": True,
            "item_key": item_key,
            "bibtex": bibtex
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Error exporting to BibTeX: {str(e)}"
        }


def tool_read_local_zotero_db(zotero_data_dir: Optional[str] = None) -> dict:
    """
    Reads items from local Zotero database (SQLite).
    
    This is for local Zotero installations. No API key required.
    Note: Zotero must be closed while reading the database.

    Args:
        zotero_data_dir (Optional[str]): Path to Zotero data directory. 
                                        If None, attempts to find default location.

    Returns:
        dict: Dictionary containing items or error message.
    """
    try:
        import sqlite3
        
        if zotero_data_dir is None:
            # Try to find default Zotero data directory
            home = Path.home()
            possible_paths = [
                home / "Zotero",
                home / ".zotero" / "zotero",
                home / "AppData" / "Roaming" / "Zotero" / "Zotero" / "Profiles"
            ]
            
            zotero_data_dir = None
            for path in possible_paths:
                if path.exists():
                    zotero_data_dir = str(path)
                    break
            
            if zotero_data_dir is None:
                return {
                    "success": False,
                    "error": "Could not find Zotero data directory. Please specify zotero_data_dir parameter."
                }
        
        db_path = Path(zotero_data_dir) / "zotero.sqlite"
        
        if not db_path.exists():
            return {
                "success": False,
                "error": f"Zotero database not found at {db_path}"
            }
        
        # Connect to database (read-only)
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        cursor = conn.cursor()
        
        # Query items
        cursor.execute("""
            SELECT i.itemID, idv.value as title
            FROM items i
            LEFT JOIN itemData id ON i.itemID = id.itemID
            LEFT JOIN itemDataValues idv ON id.valueID = idv.valueID
            LEFT JOIN fields f ON id.fieldID = f.fieldID
            WHERE f.fieldName = 'title'
            LIMIT 100
        """)
        
        items = []
        for row in cursor.fetchall():
            items.append({
                "item_id": row[0],
                "title": row[1]
            })
        
        conn.close()
        
        return {
            "success": True,
            "database_path": str(db_path),
            "count": len(items),
            "items": items,
            "note": "This is a simplified view. Use Zotero API for full item details."
        }
        
    except ImportError:
        return {
            "success": False,
            "error": "sqlite3 module not available."
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error reading local Zotero database: {str(e)}"
        }


def tool_check_zotero_api_status() -> dict:
    """
    Checks if Zotero API credentials are configured and valid.

    Returns:
        dict: Dictionary containing API status information.
    """
    api_key = os.environ.get("ZOTERO_API_KEY")
    user_id = os.environ.get("ZOTERO_USER_ID")
    
    if not api_key:
        return {
            "success": False,
            "configured": False,
            "error": "ZOTERO_API_KEY environment variable not set."
        }
    
    if not user_id:
        return {
            "success": False,
            "configured": False,
            "error": "ZOTERO_USER_ID environment variable not set."
        }
    
    try:
        import requests
        
        url = f"https://api.zotero.org/users/{user_id}"
        headers = {"Zotero-API-Key": api_key}
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        user_data = response.json()
        
        return {
            "success": True,
            "configured": True,
            "valid": True,
            "user_id": user_id,
            "username": user_data.get("username"),
            "message": "Zotero API credentials are valid."
        }
        
    except Exception as e:
        return {
            "success": False,
            "configured": True,
            "valid": False,
            "error": f"API credentials configured but validation failed: {str(e)}"
        }