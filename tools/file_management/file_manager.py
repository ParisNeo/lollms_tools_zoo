"""
File Management Toolset for LCP.

Provides comprehensive file and directory operations including listing,
reading, writing, copying, moving, and deleting files.
"""

import shutil
from pathlib import Path
from typing import List, Optional


def init_tools_library() -> dict:
    """
    Initializes the file management toolset.
    
    This function is called by LCP when the toolset is first loaded.
    It can be used to set up any required state or validate dependencies.
    
    Returns:
        dict: Status dictionary indicating successful initialization.
    """
    return {
        "status": "success",
        "message": "File management toolset initialized successfully.",
        "tools_count": 7
    }


def tool_list_directory(directory_path: str = ".", pattern: str = "*") -> dict:
    """
    Lists files and directories in a given path.

    Args:
        directory_path (str): Path to the directory to list. Defaults to current directory.
        pattern (str): Glob pattern to filter results. Defaults to "*" (all files).

    Returns:
        dict: Dictionary containing list of files and directories.
    """
    try:
        path = Path(directory_path)
        if not path.exists():
            return {"success": False, "error": f"Directory '{directory_path}' not found."}
        
        if not path.is_dir():
            return {"success": False, "error": f"'{directory_path}' is not a directory."}
        
        items = list(path.glob(pattern))
        files = [str(item.name) for item in items if item.is_file()]
        dirs = [str(item.name) for item in items if item.is_dir()]
        
        return {
            "success": True,
            "directory": str(path.absolute()),
            "files": sorted(files),
            "directories": sorted(dirs),
            "total_items": len(items)
        }
    except Exception as e:
        return {"success": False, "error": f"Error listing directory: {str(e)}"}


def tool_read_file(file_path: str, encoding: str = "utf-8") -> dict:
    """
    Reads the content of a text file.

    Args:
        file_path (str): Path to the file to read.
        encoding (str): File encoding. Defaults to "utf-8".

    Returns:
        dict: Dictionary containing file content or error message.
    """
    try:
        path = Path(file_path)
        if not path.exists():
            return {"success": False, "error": f"File '{file_path}' not found."}
        
        if not path.is_file():
            return {"success": False, "error": f"'{file_path}' is not a file."}
        
        content = path.read_text(encoding=encoding)
        
        return {
            "success": True,
            "file_path": str(path.absolute()),
            "content": content,
            "size_bytes": path.stat().st_size,
            "lines": len(content.splitlines())
        }
    except UnicodeDecodeError:
        return {"success": False, "error": f"Cannot decode file '{file_path}' with encoding '{encoding}'. File may be binary."}
    except Exception as e:
        return {"success": False, "error": f"Error reading file: {str(e)}"}


def tool_write_file(file_path: str, content: str, encoding: str = "utf-8", create_dirs: bool = True) -> dict:
    """
    Writes content to a file.

    Args:
        file_path (str): Path to the file to write.
        content (str): Content to write to the file.
        encoding (str): File encoding. Defaults to "utf-8".
        create_dirs (bool): Create parent directories if they don't exist. Defaults to True.

    Returns:
        dict: Dictionary indicating success or failure.
    """
    try:
        path = Path(file_path)
        
        if create_dirs:
            path.parent.mkdir(parents=True, exist_ok=True)
        
        path.write_text(content, encoding=encoding)
        
        return {
            "success": True,
            "file_path": str(path.absolute()),
            "bytes_written": len(content.encode(encoding)),
            "message": f"Successfully wrote to '{file_path}'"
        }
    except Exception as e:
        return {"success": False, "error": f"Error writing file: {str(e)}"}


def tool_copy_file(source_path: str, destination_path: str, overwrite: bool = False) -> dict:
    """
    Copies a file from source to destination.

    Args:
        source_path (str): Path to the source file.
        destination_path (str): Path to the destination.
        overwrite (bool): Overwrite destination if it exists. Defaults to False.

    Returns:
        dict: Dictionary indicating success or failure.
    """
    try:
        src = Path(source_path)
        dst = Path(destination_path)
        
        if not src.exists():
            return {"success": False, "error": f"Source file '{source_path}' not found."}
        
        if dst.exists() and not overwrite:
            return {"success": False, "error": f"Destination '{destination_path}' already exists. Set overwrite=True to replace it."}
        
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        
        return {
            "success": True,
            "source": str(src.absolute()),
            "destination": str(dst.absolute()),
            "message": f"Successfully copied '{source_path}' to '{destination_path}'"
        }
    except Exception as e:
        return {"success": False, "error": f"Error copying file: {str(e)}"}


def tool_move_file(source_path: str, destination_path: str, overwrite: bool = False) -> dict:
    """
    Moves a file from source to destination.

    Args:
        source_path (str): Path to the source file.
        destination_path (str): Path to the destination.
        overwrite (bool): Overwrite destination if it exists. Defaults to False.

    Returns:
        dict: Dictionary indicating success or failure.
    """
    try:
        src = Path(source_path)
        dst = Path(destination_path)
        
        if not src.exists():
            return {"success": False, "error": f"Source file '{source_path}' not found."}
        
        if dst.exists() and not overwrite:
            return {"success": False, "error": f"Destination '{destination_path}' already exists. Set overwrite=True to replace it."}
        
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))
        
        return {
            "success": True,
            "source": str(src.absolute()),
            "destination": str(dst.absolute()),
            "message": f"Successfully moved '{source_path}' to '{destination_path}'"
        }
    except Exception as e:
        return {"success": False, "error": f"Error moving file: {str(e)}"}


def tool_delete_file(file_path: str, confirm: bool = False) -> dict:
    """
    Deletes a file.

    Args:
        file_path (str): Path to the file to delete.
        confirm (bool): Confirmation flag. Must be True to actually delete. Defaults to False.

    Returns:
        dict: Dictionary indicating success or failure.
    """
    if not confirm:
        return {
            "success": False,
            "error": "Deletion not confirmed. Set confirm=True to delete the file.",
            "warning": f"This will permanently delete '{file_path}'"
        }
    
    try:
        path = Path(file_path)
        if not path.exists():
            return {"success": False, "error": f"File '{file_path}' not found."}
        
        if not path.is_file():
            return {"success": False, "error": f"'{file_path}' is not a file. Use tool_delete_directory for directories."}
        
        path.unlink()
        
        return {
            "success": True,
            "message": f"Successfully deleted '{file_path}'"
        }
    except Exception as e:
        return {"success": False, "error": f"Error deleting file: {str(e)}"}


def tool_get_file_info(file_path: str) -> dict:
    """
    Gets detailed information about a file.

    Args:
        file_path (str): Path to the file.

    Returns:
        dict: Dictionary containing file metadata.
    """
    try:
        path = Path(file_path)
        if not path.exists():
            return {"success": False, "error": f"File '{file_path}' not found."}
        
        stat = path.stat()
        
        return {
            "success": True,
            "file_path": str(path.absolute()),
            "name": path.name,
            "size_bytes": stat.st_size,
            "is_file": path.is_file(),
            "is_directory": path.is_dir(),
            "extension": path.suffix,
            "created_timestamp": stat.st_ctime,
            "modified_timestamp": stat.st_mtime,
            "is_hidden": path.name.startswith(".")
        }
    except Exception as e:
        return {"success": False, "error": f"Error getting file info: {str(e)}"}