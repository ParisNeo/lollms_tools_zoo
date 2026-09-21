"""
System Information Toolset for LCP.

Provides system and environment information utilities.
"""

import os
import sys
import platform
from pathlib import Path
from typing import Optional


def init_tools_library() -> dict:
    """
    Initializes the system information toolset.
    
    This function is called by LCP when the toolset is first loaded.
    It can be used to set up any required state or validate dependencies.
    
    Returns:
        dict: Status dictionary indicating successful initialization.
    """
    return {
        "status": "success",
        "message": "System information toolset initialized successfully.",
        "tools_count": 6
    }


def tool_get_system_info() -> dict:
    """
    Gets comprehensive system information.

    Returns:
        dict: Dictionary containing system information.
    """
    return {
        "success": True,
        "platform": platform.system(),
        "platform_release": platform.release(),
        "platform_version": platform.version(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "python_version": sys.version,
        "python_implementation": platform.python_implementation()
    }


def tool_get_current_directory() -> dict:
    """
    Gets the current working directory.

    Returns:
        dict: Dictionary containing current directory path.
    """
    cwd = Path.cwd()
    
    return {
        "success": True,
        "current_directory": str(cwd),
        "absolute_path": str(cwd.absolute())
    }


def tool_get_environment_variable(variable_name: str) -> dict:
    """
    Gets the value of an environment variable.

    Args:
        variable_name (str): Name of the environment variable.

    Returns:
        dict: Dictionary containing the variable value or error.
    """
    value = os.environ.get(variable_name)
    
    if value is None:
        return {
            "success": False,
            "error": f"Environment variable '{variable_name}' not found."
        }
    
    return {
        "success": True,
        "variable_name": variable_name,
        "value": value
    }


def tool_list_environment_variables(filter_pattern: Optional[str] = None) -> dict:
    """
    Lists all environment variables, optionally filtered by pattern.

    Args:
        filter_pattern (Optional[str]): Optional pattern to filter variable names (case-insensitive).

    Returns:
        dict: Dictionary containing environment variables.
    """
    env_vars = dict(os.environ)
    
    if filter_pattern:
        filter_lower = filter_pattern.lower()
        env_vars = {k: v for k, v in env_vars.items() if filter_lower in k.lower()}
    
    return {
        "success": True,
        "count": len(env_vars),
        "variables": env_vars,
        "filter_applied": filter_pattern is not None
    }


def tool_get_disk_usage(path: str = ".") -> dict:
    """
    Gets disk usage statistics for a path.

    Args:
        path (str): Path to check. Defaults to current directory.

    Returns:
        dict: Dictionary containing disk usage information.
    """
    try:
        stat = os.statvfs(path) if hasattr(os, 'statvfs') else None
        
        if stat:
            # Unix-like systems
            total = stat.f_blocks * stat.f_frsize
            free = stat.f_bfree * stat.f_frsize
            used = total - free
        else:
            # Windows
            import shutil
            total, used, free = shutil.disk_usage(path)
        
        return {
            "success": True,
            "path": str(Path(path).absolute()),
            "total_bytes": total,
            "used_bytes": used,
            "free_bytes": free,
            "total_gb": round(total / (1024**3), 2),
            "used_gb": round(used / (1024**3), 2),
            "free_gb": round(free / (1024**3), 2),
            "percent_used": round((used / total) * 100, 2)
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error getting disk usage: {str(e)}"
        }


def tool_get_python_path() -> dict:
    """
    Gets Python executable path and sys.path.

    Returns:
        dict: Dictionary containing Python path information.
    """
    return {
        "success": True,
        "executable": sys.executable,
        "version": sys.version,
        "path": sys.path,
        "prefix": sys.prefix,
        "base_prefix": sys.base_prefix
    }