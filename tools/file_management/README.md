# File Management Toolset

Comprehensive file and directory operations for the LCP framework.

## Overview

This toolset provides essential file system operations including listing, reading, writing, copying, moving, and deleting files. All operations are designed to work with relative paths within the discussion workspace.

## Tools

### `tool_list_directory`
Lists files and directories in a given path with optional pattern filtering.

**Parameters:**
- `directory_path` (str, optional): Path to directory. Defaults to current directory.
- `pattern` (str, optional): Glob pattern to filter results. Defaults to "*".

**Returns:** Dictionary with lists of files and directories.

---

### `tool_read_file`
Reads the content of a text file with encoding support.

**Parameters:**
- `file_path` (str): Path to the file to read.
- `encoding` (str, optional): File encoding. Defaults to "utf-8".

**Returns:** Dictionary with file content, size, and line count.

---

### `tool_write_file`
Writes content to a file with automatic directory creation.

**Parameters:**
- `file_path` (str): Path to the file to write.
- `content` (str): Content to write.
- `encoding` (str, optional): File encoding. Defaults to "utf-8".
- `create_dirs` (bool, optional): Create parent directories. Defaults to True.

**Returns:** Dictionary with success status and bytes written.

---

### `tool_copy_file`
Copies a file from source to destination.

**Parameters:**
- `source_path` (str): Source file path.
- `destination_path` (str): Destination path.
- `overwrite` (bool, optional): Overwrite if exists. Defaults to False.

**Returns:** Dictionary with success status.

---

### `tool_move_file`
Moves a file from source to destination.

**Parameters:**
- `source_path` (str): Source file path.
- `destination_path` (str): Destination path.
- `overwrite` (bool, optional): Overwrite if exists. Defaults to False.

**Returns:** Dictionary with success status.

---

### `tool_delete_file`
Deletes a file with confirmation requirement.

**Parameters:**
- `file_path` (str): Path to file to delete.
- `confirm` (bool, optional): Must be True to delete. Defaults to False.

**Returns:** Dictionary with success status or warning.

---

### `tool_get_file_info`
Gets detailed metadata about a file.

**Parameters:**
- `file_path` (str): Path to the file.

**Returns:** Dictionary with file metadata (size, timestamps, type, etc.).

## Usage Examples

```python
# List all Python files
tool_list_directory(directory_path=".", pattern="*.py")

# Read a configuration file
tool_read_file(file_path="config.json")

# Write data to a new file
tool_write_file(file_path="output/results.txt", content="Analysis complete")

# Copy with overwrite
tool_copy_file(source_path="data.csv", destination_path="backup/data.csv", overwrite=True)

# Safe delete (requires confirmation)
tool_delete_file(file_path="temp.txt", confirm=True)
```

## Safety Features

- **Confirmation Required**: Delete operations require explicit `confirm=True`
- **Overwrite Protection**: Copy/move operations prevent accidental overwrites by default
- **Path Validation**: All operations validate file/directory existence before execution
- **Encoding Support**: Proper handling of text encodings with error detection

## Error Handling

All tools return dictionaries with `success` boolean and descriptive `error` messages when operations fail.