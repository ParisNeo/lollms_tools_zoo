# System Information Toolset

System and environment information utilities for the LCP framework.

## Overview

This toolset provides access to system-level information including platform details, environment variables, disk usage, and Python environment information. Useful for diagnostics and environment-aware operations.

## Tools

### `tool_get_system_info`
Gets comprehensive system information.

**Parameters:** None

**Returns:** Dictionary with platform, architecture, processor, and Python version details.

---

### `tool_get_current_directory`
Gets the current working directory.

**Parameters:** None

**Returns:** Dictionary with current directory path.

---

### `tool_get_environment_variable`
Gets the value of a specific environment variable.

**Parameters:**
- `variable_name` (str): Name of the environment variable

**Returns:** Dictionary with variable value or error if not found.

---

### `tool_list_environment_variables`
Lists all environment variables with optional filtering.

**Parameters:**
- `filter_pattern` (str, optional): Filter pattern (case-insensitive)

**Returns:** Dictionary with all matching environment variables.

---

### `tool_get_disk_usage`
Gets disk usage statistics for a path.

**Parameters:**
- `path` (str, optional): Path to check. Defaults to current directory.

**Returns:** Dictionary with total, used, and free space in bytes and GB.

---

### `tool_get_python_path`
Gets Python executable path and sys.path information.

**Parameters:** None

**Returns:** Dictionary with Python executable, version, and path information.

## Usage Examples

```python
# Get system information
tool_get_system_info()

# Check current directory
tool_get_current_directory()

# Get specific environment variable
tool_get_environment_variable(variable_name="PATH")
tool_get_environment_variable(variable_name="HOME")

# List all Python-related environment variables
tool_list_environment_variables(filter_pattern="python")

# Check disk space
tool_get_disk_usage(path=".")
tool_get_disk_usage(path="C:/")

# Get Python environment details
tool_get_python_path()
```

## Platform Support

- **Windows**: Full support using `shutil.disk_usage()`
- **Unix/Linux**: Full support using `os.statvfs()`
- **macOS**: Full support using `os.statvfs()`

## Use Cases

- **Environment Diagnostics**: Verify system configuration
- **Path Resolution**: Understand current working directory context
- **Resource Monitoring**: Check available disk space
- **Configuration Discovery**: Find environment-specific settings
- **Python Environment**: Debug Python path and installation issues

## Error Handling

- **Missing Variables**: Returns error if environment variable not found
- **Invalid Paths**: Returns error for inaccessible paths
- **Permission Errors**: Gracefully handles permission-denied scenarios