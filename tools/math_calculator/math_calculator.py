"""
Math Calculator Toolset for LCP.

Provides mathematical operations, statistics, and calculations.
"""

import math
from typing import List


def init_tools_library() -> dict:
    """
    Initializes the math calculator toolset.
    
    This function is called by LCP when the toolset is first loaded.
    It can be used to set up any required state or validate dependencies.
    
    Returns:
        dict: Status dictionary indicating successful initialization.
    """
    return {
        "status": "success",
        "message": "Math calculator toolset initialized successfully.",
        "tools_count": 11
    }


def tool_add(a: float, b: float) -> dict:
    """
    Adds two numbers.

    Args:
        a (float): First number.
        b (float): Second number.

    Returns:
        dict: Dictionary containing the result.
    """
    return {
        "success": True,
        "operation": "addition",
        "a": a,
        "b": b,
        "result": a + b
    }


def tool_subtract(a: float, b: float) -> dict:
    """
    Subtracts two numbers.

    Args:
        a (float): First number.
        b (float): Second number.

    Returns:
        dict: Dictionary containing the result.
    """
    return {
        "success": True,
        "operation": "subtraction",
        "a": a,
        "b": b,
        "result": a - b
    }


def tool_multiply(a: float, b: float) -> dict:
    """
    Multiplies two numbers.

    Args:
        a (float): First number.
        b (float): Second number.

    Returns:
        dict: Dictionary containing the result.
    """
    return {
        "success": True,
        "operation": "multiplication",
        "a": a,
        "b": b,
        "result": a * b
    }


def tool_divide(a: float, b: float) -> dict:
    """
    Divides two numbers.

    Args:
        a (float): Numerator.
        b (float): Denominator.

    Returns:
        dict: Dictionary containing the result or error.
    """
    if b == 0:
        return {
            "success": False,
            "error": "Division by zero is not allowed."
        }
    
    return {
        "success": True,
        "operation": "division",
        "a": a,
        "b": b,
        "result": a / b
    }


def tool_power(base: float, exponent: float) -> dict:
    """
    Raises a number to a power.

    Args:
        base (float): The base number.
        exponent (float): The exponent.

    Returns:
        dict: Dictionary containing the result.
    """
    return {
        "success": True,
        "operation": "power",
        "base": base,
        "exponent": exponent,
        "result": base ** exponent
    }


def tool_square_root(number: float) -> dict:
    """
    Calculates the square root of a number.

    Args:
        number (float): The number.

    Returns:
        dict: Dictionary containing the result or error.
    """
    if number < 0:
        return {
            "success": False,
            "error": "Cannot calculate square root of negative number."
        }
    
    return {
        "success": True,
        "operation": "square_root",
        "number": number,
        "result": math.sqrt(number)
    }


def tool_factorial(n: int) -> dict:
    """
    Calculates the factorial of a number.

    Args:
        n (int): The number (must be non-negative integer).

    Returns:
        dict: Dictionary containing the result or error.
    """
    if n < 0:
        return {
            "success": False,
            "error": "Factorial is not defined for negative numbers."
        }
    
    return {
        "success": True,
        "operation": "factorial",
        "n": n,
        "result": math.factorial(n)
    }


def tool_calculate_mean(numbers: List[float]) -> dict:
    """
    Calculates the arithmetic mean of a list of numbers.

    Args:
        numbers (List[float]): List of numbers.

    Returns:
        dict: Dictionary containing the mean.
    """
    if not numbers:
        return {
            "success": False,
            "error": "Cannot calculate mean of empty list."
        }
    
    return {
        "success": True,
        "operation": "mean",
        "count": len(numbers),
        "sum": sum(numbers),
        "mean": sum(numbers) / len(numbers)
    }


def tool_calculate_median(numbers: List[float]) -> dict:
    """
    Calculates the median of a list of numbers.

    Args:
        numbers (List[float]): List of numbers.

    Returns:
        dict: Dictionary containing the median.
    """
    if not numbers:
        return {
            "success": False,
            "error": "Cannot calculate median of empty list."
        }
    
    sorted_nums = sorted(numbers)
    n = len(sorted_nums)
    
    if n % 2 == 0:
        median = (sorted_nums[n//2 - 1] + sorted_nums[n//2]) / 2
    else:
        median = sorted_nums[n//2]
    
    return {
        "success": True,
        "operation": "median",
        "count": n,
        "median": median
    }


def tool_calculate_std_dev(numbers: List[float]) -> dict:
    """
    Calculates the standard deviation of a list of numbers.

    Args:
        numbers (List[float]): List of numbers.

    Returns:
        dict: Dictionary containing the standard deviation.
    """
    if len(numbers) < 2:
        return {
            "success": False,
            "error": "Need at least 2 numbers to calculate standard deviation."
        }
    
    mean = sum(numbers) / len(numbers)
    variance = sum((x - mean) ** 2 for x in numbers) / (len(numbers) - 1)
    std_dev = math.sqrt(variance)
    
    return {
        "success": True,
        "operation": "standard_deviation",
        "count": len(numbers),
        "mean": mean,
        "variance": variance,
        "std_dev": std_dev
    }


def tool_calculate_percentage(part: float, whole: float) -> dict:
    """
    Calculates what percentage 'part' is of 'whole'.

    Args:
        part (float): The part value.
        whole (float): The whole value.

    Returns:
        dict: Dictionary containing the percentage.
    """
    if whole == 0:
        return {
            "success": False,
            "error": "Cannot calculate percentage when whole is zero."
        }
    
    percentage = (part / whole) * 100
    
    return {
        "success": True,
        "operation": "percentage",
        "part": part,
        "whole": whole,
        "percentage": percentage
    }