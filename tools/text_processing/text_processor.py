"""
Text Processing Toolset for LCP.

Provides text manipulation, analysis, and transformation utilities.
"""

import re
from typing import List, Optional
from collections import Counter


def init_tools_library() -> dict:
    """
    Initializes the text processing toolset.
    
    This function is called by LCP when the toolset is first loaded.
    It can be used to set up any required state or validate dependencies.
    
    Returns:
        dict: Status dictionary indicating successful initialization.
    """
    return {
        "status": "success",
        "message": "Text processing toolset initialized successfully.",
        "tools_count": 10
    }


def tool_count_words(text: str) -> dict:
    """
    Counts words, characters, and lines in text.

    Args:
        text (str): The text to analyze.

    Returns:
        dict: Dictionary containing text statistics.
    """
    words = text.split()
    lines = text.splitlines()
    
    return {
        "success": True,
        "word_count": len(words),
        "character_count": len(text),
        "character_count_no_spaces": len(text.replace(" ", "")),
        "line_count": len(lines),
        "paragraph_count": len([p for p in text.split("\n\n") if p.strip()])
    }


def tool_find_replace(text: str, find: str, replace: str, case_sensitive: bool = True) -> dict:
    """
    Finds and replaces text.

    Args:
        text (str): The original text.
        find (str): Text to find.
        replace (str): Text to replace with.
        case_sensitive (bool): Whether search is case-sensitive. Defaults to True.

    Returns:
        dict: Dictionary containing modified text and replacement count.
    """
    if case_sensitive:
        count = text.count(find)
        result = text.replace(find, replace)
    else:
        pattern = re.compile(re.escape(find), re.IGNORECASE)
        count = len(pattern.findall(text))
        result = pattern.sub(replace, text)
    
    return {
        "success": True,
        "original_text": text,
        "modified_text": result,
        "replacements_made": count
    }


def tool_extract_emails(text: str) -> dict:
    """
    Extracts email addresses from text.

    Args:
        text (str): The text to search.

    Returns:
        dict: Dictionary containing list of found email addresses.
    """
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(pattern, text)
    
    return {
        "success": True,
        "emails": emails,
        "count": len(emails)
    }


def tool_extract_urls(text: str) -> dict:
    """
    Extracts URLs from text.

    Args:
        text (str): The text to search.

    Returns:
        dict: Dictionary containing list of found URLs.
    """
    pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    urls = re.findall(pattern, text)
    
    return {
        "success": True,
        "urls": urls,
        "count": len(urls)
    }


def tool_text_statistics(text: str) -> dict:
    """
    Provides detailed statistics about text.

    Args:
        text (str): The text to analyze.

    Returns:
        dict: Dictionary containing detailed text statistics.
    """
    words = text.split()
    word_lengths = [len(word) for word in words]
    
    # Most common words
    word_freq = Counter(words)
    most_common = word_freq.most_common(10)
    
    return {
        "success": True,
        "total_words": len(words),
        "unique_words": len(set(words)),
        "average_word_length": sum(word_lengths) / len(word_lengths) if word_lengths else 0,
        "longest_word": max(words, key=len) if words else "",
        "shortest_word": min(words, key=len) if words else "",
        "most_common_words": [{"word": word, "count": count} for word, count in most_common]
    }


def tool_to_uppercase(text: str) -> dict:
    """
    Converts text to uppercase.

    Args:
        text (str): The text to convert.

    Returns:
        dict: Dictionary containing converted text.
    """
    return {
        "success": True,
        "original": text,
        "converted": text.upper()
    }


def tool_to_lowercase(text: str) -> dict:
    """
    Converts text to lowercase.

    Args:
        text (str): The text to convert.

    Returns:
        dict: Dictionary containing converted text.
    """
    return {
        "success": True,
        "original": text,
        "converted": text.lower()
    }


def tool_to_title_case(text: str) -> dict:
    """
    Converts text to title case.

    Args:
        text (str): The text to convert.

    Returns:
        dict: Dictionary containing converted text.
    """
    return {
        "success": True,
        "original": text,
        "converted": text.title()
    }


def tool_reverse_text(text: str) -> dict:
    """
    Reverses text.

    Args:
        text (str): The text to reverse.

    Returns:
        dict: Dictionary containing reversed text.
    """
    return {
        "success": True,
        "original": text,
        "reversed": text[::-1]
    }


def tool_remove_whitespace(text: str, mode: str = "strip") -> dict:
    """
    Removes whitespace from text.

    Args:
        text (str): The text to process.
        mode (str): Mode of whitespace removal: "strip" (leading/trailing), "all" (all spaces), "extra" (multiple spaces to single). Defaults to "strip".

    Returns:
        dict: Dictionary containing processed text.
    """
    if mode == "strip":
        result = text.strip()
    elif mode == "all":
        result = text.replace(" ", "").replace("\t", "").replace("\n", "")
    elif mode == "extra":
        result = re.sub(r'\s+', ' ', text).strip()
    else:
        return {"success": False, "error": f"Invalid mode '{mode}'. Use 'strip', 'all', or 'extra'."}
    
    return {
        "success": True,
        "original": text,
        "processed": result,
        "mode": mode
    }