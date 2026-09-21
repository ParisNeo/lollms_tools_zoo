# Text Processing Toolset

Text manipulation, analysis, and transformation utilities for the LCP framework.

## Overview

This toolset provides comprehensive text processing capabilities including statistical analysis, pattern extraction, case conversion, and text transformation. All operations are Unicode-aware and handle edge cases gracefully.

## Tools

### Analysis Tools

#### `tool_count_words`
Counts words, characters, lines, and paragraphs in text.

**Parameters:**
- `text` (str): Text to analyze

**Returns:** Dictionary with word count, character counts, line count, and paragraph count.

---

#### `tool_text_statistics`
Provides detailed statistical analysis of text.

**Parameters:**
- `text` (str): Text to analyze

**Returns:** Dictionary with total words, unique words, average word length, longest/shortest words, and most common words.

---

### Pattern Extraction

#### `tool_extract_emails`
Extracts email addresses from text using regex.

**Parameters:**
- `text` (str): Text to search

**Returns:** Dictionary with list of found emails and count.

---

#### `tool_extract_urls`
Extracts URLs from text using regex.

**Parameters:**
- `text` (str): Text to search

**Returns:** Dictionary with list of found URLs and count.

---

### Text Transformation

#### `tool_find_replace`
Finds and replaces text with case-sensitivity option.

**Parameters:**
- `text` (str): Original text
- `find` (str): Text to find
- `replace` (str): Replacement text
- `case_sensitive` (bool, optional): Case-sensitive search. Defaults to True.

**Returns:** Dictionary with modified text and replacement count.

---

#### `tool_to_uppercase`
Converts text to uppercase.

**Parameters:**
- `text` (str): Text to convert

**Returns:** Dictionary with converted text.

---

#### `tool_to_lowercase`
Converts text to lowercase.

**Parameters:**
- `text` (str): Text to convert

**Returns:** Dictionary with converted text.

---

#### `tool_to_title_case`
Converts text to title case.

**Parameters:**
- `text` (str): Text to convert

**Returns:** Dictionary with converted text.

---

#### `tool_reverse_text`
Reverses text character by character.

**Parameters:**
- `text` (str): Text to reverse

**Returns:** Dictionary with reversed text.

---

#### `tool_remove_whitespace`
Removes whitespace with multiple modes.

**Parameters:**
- `text` (str): Text to process
- `mode` (str, optional): "strip" (leading/trailing), "all" (all whitespace), or "extra" (multiple to single). Defaults to "strip".

**Returns:** Dictionary with processed text or error for invalid mode.

## Usage Examples

```python
# Text analysis
text = "The quick brown fox jumps over the lazy dog. The dog was not amused."
tool_count_words(text=text)
tool_text_statistics(text=text)

# Pattern extraction
content = "Contact us at support@example.com or visit https://example.com"
tool_extract_emails(text=content)
tool_extract_urls(text=content)

# Find and replace
tool_find_replace(text="Hello World", find="World", replace="Universe")
tool_find_replace(text="Hello HELLO hello", find="hello", replace="hi", case_sensitive=False)

# Case conversion
tool_to_uppercase(text="hello world")
tool_to_lowercase(text="HELLO WORLD")
tool_to_title_case(text="hello world")

# Text transformation
tool_reverse_text(text="Python")
tool_remove_whitespace(text="  multiple   spaces  ", mode="extra")
```

## Features

- **Unicode Support**: All operations handle Unicode text correctly
- **Regex Patterns**: Robust email and URL extraction
- **Flexible Modes**: Multiple whitespace removal modes
- **Case Control**: Optional case-sensitive operations
- **Statistical Analysis**: Comprehensive text statistics

## Error Handling

- **Invalid Modes**: Returns error for unsupported whitespace removal modes
- **Empty Text**: Gracefully handles empty strings
- **Pattern Matching**: Returns empty lists when no patterns found