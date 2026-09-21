"""
Universal Calculator Toolset for LoLLMS.

This module provides a powerful, safe mathematical expression evaluator that can
handle complex formulas including arithmetic, algebra, trigonometry, logarithms,
and more. It uses AST parsing to safely evaluate expressions without exec/eval.

Features:
- Safe expression evaluation (no arbitrary code execution)
- Support for mathematical constants (pi, e, tau, inf)
- Trigonometric functions (sin, cos, tan, asin, acos, atan, atan2)
- Hyperbolic functions (sinh, cosh, tanh, asinh, acosh, atanh)
- Logarithmic functions (log, log10, log2, ln)
- Exponential and power functions (exp, sqrt, pow)
- Statistical functions (abs, floor, ceil, round)
- Complex number support
- Unit conversion helpers
- Expression simplification and formatting
"""

import ast
import math
import operator
import re
from typing import Any, Dict, List, Optional, Union, Callable
from dataclasses import dataclass
from enum import Enum


class CalculationError(Exception):
    """Custom exception for calculation errors."""
    pass


class AngleUnit(Enum):
    """Angle unit for trigonometric calculations."""
    RADIANS = "radians"
    DEGREES = "degrees"


@dataclass
class CalculationResult:
    """Result of a calculation with metadata."""
    expression: str
    result: Union[float, int, complex, str]
    result_type: str
    steps: List[str]
    success: bool
    error: Optional[str] = None


class SafeExpressionEvaluator:
    """
    Safe mathematical expression evaluator using AST parsing.
    
    This class parses mathematical expressions into an Abstract Syntax Tree (AST)
    and evaluates them safely without using exec() or eval(), preventing arbitrary
    code execution.
    """
    
    # Supported binary operators
    BINARY_OPERATORS: Dict[type, Callable] = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
    }
    
    # Supported unary operators
    UNARY_OPERATORS: Dict[type, Callable] = {
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
        ast.Invert: operator.invert,
    }
    
    # Supported comparison operators
    COMPARISON_OPERATORS: Dict[type, Callable] = {
        ast.Eq: operator.eq,
        ast.NotEq: operator.ne,
        ast.Lt: operator.lt,
        ast.LtE: operator.le,
        ast.Gt: operator.gt,
        ast.GtE: operator.ge,
    }
    
    # Mathematical constants
    CONSTANTS: Dict[str, Union[float, complex]] = {
        'pi': math.pi,
        'e': math.e,
        'tau': math.tau,
        'inf': math.inf,
        'infinity': math.inf,
        'nan': math.nan,
        'i': complex(0, 1),
        'j': complex(0, 1),
    }
    
    # Mathematical functions
    FUNCTIONS: Dict[str, Callable] = {
        # Basic math
        'abs': abs,
        'round': round,
        'floor': math.floor,
        'ceil': math.ceil,
        'trunc': math.trunc,
        
        # Power and roots
        'sqrt': math.sqrt,
        'cbrt': lambda x: math.copysign(abs(x) ** (1/3), x),
        'pow': pow,
        'exp': math.exp,
        'expm1': math.expm1,
        
        # Logarithms
        'log': math.log,
        'ln': math.log,
        'log10': math.log10,
        'log2': math.log2,
        'log1p': math.log1p,
        
        # Trigonometric (radians)
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'asin': math.asin,
        'acos': math.acos,
        'atan': math.atan,
        'atan2': math.atan2,
        
        # Hyperbolic
        'sinh': math.sinh,
        'cosh': math.cosh,
        'tanh': math.tanh,
        'asinh': math.asinh,
        'acosh': math.acosh,
        'atanh': math.atanh,
        
        # Special functions
        'factorial': math.factorial,
        'gamma': math.gamma,
        'lgamma': math.lgamma,
        'erf': math.erf,
        'erfc': math.erfc,
        
        # Combinatorics
        'comb': math.comb,
        'perm': math.perm,
        'gcd': math.gcd,
        'lcm': math.lcm,
        
        # Geometry
        'hypot': math.hypot,
        'dist': lambda x1, y1, x2, y2: math.hypot(x2 - x1, y2 - y1),
        
        # Complex number functions
        'real': lambda x: x.real if isinstance(x, complex) else x,
        'imag': lambda x: x.imag if isinstance(x, complex) else 0,
        'conj': lambda x: x.conjugate() if isinstance(x, complex) else x,
        'phase': lambda x: math.atan2(x.imag, x.real) if isinstance(x, complex) else 0,
        'abs_complex': abs,
        
        # Utility
        'min': min,
        'max': max,
        'sum': sum,
        'sign': lambda x: (x > 0) - (x < 0),
        'clamp': lambda x, lo, hi: max(lo, min(hi, x)),
    }
    
    # Degree-based trigonometric functions
    DEG_FUNCTIONS: Dict[str, Callable] = {
        'sind': lambda x: math.sin(math.radians(x)),
        'cosd': lambda x: math.cos(math.radians(x)),
        'tand': lambda x: math.tan(math.radians(x)),
        'asind': lambda x: math.degrees(math.asin(x)),
        'acosd': lambda x: math.degrees(math.acos(x)),
        'atand': lambda x: math.degrees(math.atan(x)),
        'atan2d': lambda y, x: math.degrees(math.atan2(y, x)),
    }
    
    def __init__(self, angle_unit: AngleUnit = AngleUnit.RADIANS):
        """
        Initialize the evaluator.
        
        Args:
            angle_unit: Default angle unit for trigonometric functions.
        """
        self.angle_unit = angle_unit
        self._all_functions = {**self.FUNCTIONS, **self.DEG_FUNCTIONS}
    
    def evaluate(self, expression: str) -> Union[float, int, complex]:
        """
        Safely evaluate a mathematical expression.
        
        Args:
            expression: The mathematical expression to evaluate.
            
        Returns:
            The result of the evaluation.
            
        Raises:
            CalculationError: If the expression is invalid or cannot be evaluated.
        """
        try:
            # Preprocess the expression
            processed = self._preprocess(expression)
            
            # Parse into AST
            tree = ast.parse(processed, mode='eval')
            
            # Validate the AST
            self._validate_node(tree)
            
            # Evaluate
            result = self._eval_node(tree.body)
            
            return result
            
        except SyntaxError as e:
            raise CalculationError(f"Invalid syntax: {e}")
        except CalculationError:
            raise
        except Exception as e:
            raise CalculationError(f"Evaluation error: {e}")
    
    def _preprocess(self, expression: str) -> str:
        """
        Preprocess the expression string.
        
        Handles common mathematical notations and converts them to Python syntax.
        """
        # Remove whitespace
        expr = expression.strip()
        
        # Replace common notations
        replacements = [
            # Implicit multiplication: 2(3) -> 2*(3), 2x -> 2*x
            (r'(\d)\s*\(', r'\1*('),
            (r'\)\s*\(', r')*('),
            (r'\)\s*(\d)', r')*\1'),
            
            # Caret to power: 2^3 -> 2**3
            (r'\^', '**'),
            
            # Percentage: 50% -> 0.5
            (r'(\d+(?:\.\d+)?)\s*%', r'(\1/100)'),
        ]
        
        for pattern, replacement in replacements:
            expr = re.sub(pattern, replacement, expr)
        
        return expr
    
    def _validate_node(self, node: ast.AST) -> None:
        """
        Validate that the AST only contains allowed operations.
        
        Args:
            node: The AST node to validate.
            
        Raises:
            CalculationError: If the node contains disallowed operations.
        """
        allowed_nodes = (
            ast.Expression, ast.BinOp, ast.UnaryOp, ast.Call, ast.Load,
            ast.Constant, ast.Num, ast.Name, ast.Compare,
            # Operators
            ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Mod, ast.Pow,
            ast.UAdd, ast.USub, ast.Invert,
            ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
            # Collections for functions like sum, min, max
            ast.List, ast.Tuple,
        )
        
        for child in ast.walk(node):
            if not isinstance(child, allowed_nodes):
                raise CalculationError(
                    f"Disallowed operation: {type(child).__name__}"
                )
            
            # Check for disallowed names
            if isinstance(child, ast.Name):
                if child.id.startswith('_'):
                    raise CalculationError(
                        f"Access to private names is not allowed: {child.id}"
                    )
    
    def _eval_node(self, node: ast.AST) -> Union[float, int, complex, List]:
        """
        Recursively evaluate an AST node.
        
        Args:
            node: The AST node to evaluate.
            
        Returns:
            The evaluated result.
        """
        if isinstance(node, ast.Constant):
            return node.value
        
        elif isinstance(node, ast.Num):  # Python < 3.8 compatibility
            return node.n
        
        elif isinstance(node, ast.Name):
            name = node.id.lower()
            if name in self.CONSTANTS:
                return self.CONSTANTS[name]
            raise CalculationError(f"Unknown variable: {node.id}")
        
        elif isinstance(node, ast.BinOp):
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            op_type = type(node.op)
            
            if op_type not in self.BINARY_OPERATORS:
                raise CalculationError(f"Unsupported operator: {op_type.__name__}")
            
            try:
                return self.BINARY_OPERATORS[op_type](left, right)
            except ZeroDivisionError:
                raise CalculationError("Division by zero")
            except OverflowError:
                raise CalculationError("Numerical overflow")
        
        elif isinstance(node, ast.UnaryOp):
            operand = self._eval_node(node.operand)
            op_type = type(node.op)
            
            if op_type not in self.UNARY_OPERATORS:
                raise CalculationError(f"Unsupported unary operator: {op_type.__name__}")
            
            return self.UNARY_OPERATORS[op_type](operand)
        
        elif isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise CalculationError("Only direct function calls are allowed")
            
            func_name = node.func.id.lower()
            
            if func_name not in self._all_functions:
                raise CalculationError(f"Unknown function: {node.func.id}")
            
            func = self._all_functions[func_name]
            args = [self._eval_node(arg) for arg in node.args]
            
            try:
                return func(*args)
            except TypeError as e:
                raise CalculationError(f"Invalid arguments for {func_name}: {e}")
            except ValueError as e:
                raise CalculationError(f"Math domain error in {func_name}: {e}")
        
        elif isinstance(node, ast.Compare):
            left = self._eval_node(node.left)
            
            for op, comparator in zip(node.ops, node.comparators):
                right = self._eval_node(comparator)
                op_type = type(op)
                
                if op_type not in self.COMPARISON_OPERATORS:
                    raise CalculationError(f"Unsupported comparison: {op_type.__name__}")
                
                if not self.COMPARISON_OPERATORS[op_type](left, right):
                    return 0  # False
                left = right
            
            return 1  # True
        
        elif isinstance(node, ast.List):
            return [self._eval_node(elt) for elt in node.elts]
        
        elif isinstance(node, ast.Tuple):
            return tuple(self._eval_node(elt) for elt in node.elts)
        
        else:
            raise CalculationError(f"Unsupported expression type: {type(node).__name__}")


# Global evaluator instance
_evaluator: Optional[SafeExpressionEvaluator] = None


def init_tools_library() -> bool:
    """
    Initialize the calculator tools library.
    
    This function is called by LCP when the toolset is first invoked.
    It performs lazy initialization of heavy resources.
    
    Returns:
        True if initialization was successful, False otherwise.
    """
    global _evaluator
    try:
        _evaluator = SafeExpressionEvaluator()
        return True
    except Exception:
        return False


def _get_evaluator() -> SafeExpressionEvaluator:
    """Get or create the global evaluator instance."""
    global _evaluator
    if _evaluator is None:
        _evaluator = SafeExpressionEvaluator()
    return _evaluator


def calculate(expression: str) -> Dict[str, Any]:
    """
    Evaluate a complex mathematical expression and return the result.
    
    This is the main universal calculator tool that can handle:
    - Basic arithmetic: 2 + 3 * 4, (5 + 3) / 2
    - Powers and roots: 2^10, sqrt(16), cbrt(27)
    - Trigonometry: sin(pi/4), cos(0), tan(pi/6)
    - Logarithms: log(e^2), log10(100), ln(e)
    - Exponentials: exp(1), e^5
    - Constants: pi, e, tau, inf
    - Complex numbers: 3+4j, abs(3+4j), real(2+3j)
    - Factorials and combinatorics: factorial(5), comb(10, 3)
    - Statistical: min(1,2,3), max([1,5,3]), sum([1,2,3,4])
    
    Args:
        expression: A mathematical expression as a string.
                   Supports standard mathematical notation including:
                   - Operators: +, -, *, /, //, %, ^ or **
                   - Functions: sin, cos, tan, log, ln, sqrt, exp, abs, etc.
                   - Constants: pi, e, tau, inf
                   - Parentheses for grouping
                   - Implicit multiplication: 2(3) = 6
                   - Percentages: 50% = 0.5
    
    Returns:
        A dictionary containing:
        - success: Whether the calculation succeeded
        - expression: The original expression
        - result: The calculated result (if successful)
        - result_type: The type of result (integer, float, complex)
        - formatted: Human-readable formatted result
        - error: Error message (if failed)
    
    Examples:
        >>> calculate("2 + 3 * 4")
        {'success': True, 'result': 14, ...}
        
        >>> calculate("sqrt(16) + sin(pi/2)")
        {'success': True, 'result': 5.0, ...}
        
        >>> calculate("factorial(10) / comb(10, 3)")
        {'success': True, 'result': 30240.0, ...}
    """
    try:
        evaluator = _get_evaluator()
        result = evaluator.evaluate(expression)
        
        # Determine result type
        if isinstance(result, complex):
            result_type = "complex"
            formatted = _format_complex(result)
        elif isinstance(result, int):
            result_type = "integer"
            formatted = str(result)
        elif isinstance(result, float):
            result_type = "float"
            formatted = _format_float(result)
        elif isinstance(result, (list, tuple)):
            result_type = "sequence"
            formatted = str(result)
        else:
            result_type = type(result).__name__
            formatted = str(result)
        
        return {
            "success": True,
            "expression": expression,
            "result": result,
            "result_type": result_type,
            "formatted": formatted,
            "error": None
        }
        
    except CalculationError as e:
        return {
            "success": False,
            "expression": expression,
            "result": None,
            "result_type": None,
            "formatted": None,
            "error": str(e)
        }
    except Exception as e:
        return {
            "success": False,
            "expression": expression,
            "result": None,
            "result_type": None,
            "formatted": None,
            "error": f"Unexpected error: {str(e)}"
        }


def calculate_with_steps(expression: str) -> Dict[str, Any]:
    """
    Evaluate a mathematical expression and return detailed calculation steps.
    
    This tool provides a step-by-step breakdown of how the expression is evaluated,
    useful for educational purposes or debugging complex formulas.
    
    Args:
        expression: A mathematical expression as a string.
    
    Returns:
        A dictionary containing:
        - success: Whether the calculation succeeded
        - expression: The original expression
        - result: The calculated result
        - steps: List of calculation steps
        - error: Error message (if failed)
    
    Examples:
        >>> calculate_with_steps("2 + 3 * 4")
        {'success': True, 'steps': ['3 * 4 = 12', '2 + 12 = 14'], 'result': 14}
    """
    try:
        evaluator = _get_evaluator()
        steps: List[str] = []
        
        # Parse and analyze the expression
        processed = evaluator._preprocess(expression)
        tree = ast.parse(processed, mode='eval')
        
        # Extract steps from the AST
        _extract_steps(tree.body, evaluator, steps)
        
        # Evaluate the final result
        result = evaluator.evaluate(expression)
        
        return {
            "success": True,
            "expression": expression,
            "result": result,
            "result_type": type(result).__name__,
            "formatted": _format_float(result) if isinstance(result, float) else str(result),
            "steps": steps,
            "error": None
        }
        
    except Exception as e:
        return {
            "success": False,
            "expression": expression,
            "result": None,
            "steps": [],
            "error": str(e)
        }


def _extract_steps(node: ast.AST, evaluator: SafeExpressionEvaluator, 
                   steps: List[str], depth: int = 0) -> Union[float, int, complex]:
    """Extract calculation steps from an AST node."""
    if isinstance(node, ast.BinOp):
        left = _extract_steps(node.left, evaluator, steps, depth + 1)
        right = _extract_steps(node.right, evaluator, steps, depth + 1)
        op_type = type(node.op)
        op_symbols = {
            ast.Add: '+', ast.Sub: '-', ast.Mult: '*', ast.Div: '/',
            ast.FloorDiv: '//', ast.Mod: '%', ast.Pow: '^'
        }
        op_sym = op_symbols.get(op_type, '?')
        result = evaluator.BINARY_OPERATORS[op_type](left, right)
        steps.append(f"{_format_number(left)} {op_sym} {_format_number(right)} = {_format_number(result)}")
        return result
    
    elif isinstance(node, ast.UnaryOp):
        operand = _extract_steps(node.operand, evaluator, steps, depth + 1)
        op_type = type(node.op)
        result = evaluator.UNARY_OPERATORS[op_type](operand)
        op_sym = '-' if isinstance(node.op, ast.USub) else '+'
        steps.append(f"{op_sym}{_format_number(operand)} = {_format_number(result)}")
        return result
    
    elif isinstance(node, ast.Call):
        func_name = node.func.id
        args = [_extract_steps(arg, evaluator, steps, depth + 1) for arg in node.args]
        func = evaluator._all_functions.get(func_name.lower())
        if func:
            result = func(*args)
            args_str = ', '.join(_format_number(a) for a in args)
            steps.append(f"{func_name}({args_str}) = {_format_number(result)}")
            return result
        raise CalculationError(f"Unknown function: {func_name}")
    
    elif isinstance(node, ast.Constant):
        return node.value
    
    elif isinstance(node, ast.Name):
        return evaluator.CONSTANTS.get(node.id.lower(), 0)
    
    return 0


def convert_units(value: float, from_unit: str, to_unit: str) -> Dict[str, Any]:
    """
    Convert a value between different units of measurement.
    
    Supports conversions for:
    - Length: mm, cm, m, km, in, ft, yd, mi
    - Mass: mg, g, kg, t, oz, lb
    - Temperature: C, F, K
    - Time: ms, s, min, hr, day, week, year
    - Data: B, KB, MB, GB, TB
    - Angle: deg, rad, grad
    
    Args:
        value: The numeric value to convert.
        from_unit: The source unit (e.g., 'km', 'lb', 'F').
        to_unit: The target unit (e.g., 'mi', 'kg', 'C').
    
    Returns:
        A dictionary containing:
        - success: Whether the conversion succeeded
        - original_value: The input value
        - original_unit: The source unit
        - converted_value: The converted value
        - converted_unit: The target unit
        - error: Error message (if failed)
    
    Examples:
        >>> convert_units(100, 'km', 'mi')
        {'success': True, 'converted_value': 62.137...}
        
        >>> convert_units(32, 'F', 'C')
        {'success': True, 'converted_value': 0.0}
    """
    # Conversion factors to base units
    conversions = {
        # Length (base: meters)
        'mm': ('length', 0.001), 'cm': ('length', 0.01), 'm': ('length', 1.0),
        'km': ('length', 1000.0), 'in': ('length', 0.0254), 'ft': ('length', 0.3048),
        'yd': ('length', 0.9144), 'mi': ('length', 1609.344),
        
        # Mass (base: grams)
        'mg': ('mass', 0.001), 'g': ('mass', 1.0), 'kg': ('mass', 1000.0),
        't': ('mass', 1000000.0), 'oz': ('mass', 28.349523125), 'lb': ('mass', 453.59237),
        
        # Time (base: seconds)
        'ms': ('time', 0.001), 's': ('time', 1.0), 'min': ('time', 60.0),
        'hr': ('time', 3600.0), 'day': ('time', 86400.0),
        'week': ('time', 604800.0), 'year': ('time', 31557600.0),
        
        # Data (base: bytes)
        'B': ('data', 1.0), 'KB': ('data', 1024.0), 'MB': ('data', 1048576.0),
        'GB': ('data', 1073741824.0), 'TB': ('data', 1099511627776.0),
        
        # Angle (base: radians)
        'rad': ('angle', 1.0), 'deg': ('angle', math.pi / 180),
        'grad': ('angle', math.pi / 200),
    }
    
    from_lower = from_unit.lower()
    to_lower = to_unit.lower()
    
    # Special case: Temperature
    if from_lower in ('c', 'f', 'k') and to_lower in ('c', 'f', 'k'):
        return _convert_temperature(value, from_lower, to_lower)
    
    # Check if units exist
    if from_lower not in conversions:
        return {
            "success": False,
            "error": f"Unknown unit: {from_unit}",
            "supported_units": list(conversions.keys()) + ['C', 'F', 'K']
        }
    
    if to_lower not in conversions:
        return {
            "success": False,
            "error": f"Unknown unit: {to_unit}",
            "supported_units": list(conversions.keys()) + ['C', 'F', 'K']
        }
    
    from_category, from_factor = conversions[from_lower]
    to_category, to_factor = conversions[to_lower]
    
    # Check if units are in the same category
    if from_category != to_category:
        return {
            "success": False,
            "error": f"Cannot convert between {from_category} and {to_category}"
        }
    
    # Perform conversion
    base_value = value * from_factor
    converted_value = base_value / to_factor
    
    return {
        "success": True,
        "original_value": value,
        "original_unit": from_unit,
        "converted_value": converted_value,
        "converted_unit": to_unit,
        "formatted": f"{value} {from_unit} = {_format_float(converted_value)} {to_unit}",
        "error": None
    }


def _convert_temperature(value: float, from_unit: str, to_unit: str) -> Dict[str, Any]:
    """Convert temperature between Celsius, Fahrenheit, and Kelvin."""
    # Convert to Celsius first
    if from_unit == 'f':
        celsius = (value - 32) * 5 / 9
    elif from_unit == 'k':
        celsius = value - 273.15
    else:
        celsius = value
    
    # Convert from Celsius to target
    if to_unit == 'f':
        result = celsius * 9 / 5 + 32
    elif to_unit == 'k':
        result = celsius + 273.15
    else:
        result = celsius
    
    return {
        "success": True,
        "original_value": value,
        "original_unit": from_unit.upper(),
        "converted_value": result,
        "converted_unit": to_unit.upper(),
        "formatted": f"{value}°{from_unit.upper()} = {_format_float(result)}°{to_unit.upper()}",
        "error": None
    }


def solve_quadratic(a: float, b: float, c: float) -> Dict[str, Any]:
    """
    Solve a quadratic equation of the form ax² + bx + c = 0.
    
    Args:
        a: Coefficient of x²
        b: Coefficient of x
        c: Constant term
    
    Returns:
        A dictionary containing:
        - success: Whether the equation could be solved
        - equation: The formatted equation string
        - discriminant: The discriminant (b² - 4ac)
        - num_solutions: Number of real solutions (0, 1, or 2)
        - solutions: List of solutions (may include complex numbers)
        - error: Error message (if failed)
    
    Examples:
        >>> solve_quadratic(1, -5, 6)  # x² - 5x + 6 = 0
        {'success': True, 'solutions': [3.0, 2.0], ...}
        
        >>> solve_quadratic(1, 0, 1)  # x² + 1 = 0
        {'success': True, 'solutions': [1j, -1j], ...}
    """
    if a == 0:
        return {
            "success": False,
            "error": "Coefficient 'a' cannot be zero (not a quadratic equation)",
            "equation": f"{b}x + {c} = 0"
        }
    
    equation = f"{a}x² + {b}x + {c} = 0"
    discriminant = b**2 - 4*a*c
    
    if discriminant > 0:
        # Two real solutions
        x1 = (-b + math.sqrt(discriminant)) / (2*a)
        x2 = (-b - math.sqrt(discriminant)) / (2*a)
        solutions = [x1, x2]
        num_solutions = 2
        solution_type = "real"
    elif discriminant == 0:
        # One real solution (repeated root)
        x = -b / (2*a)
        solutions = [x]
        num_solutions = 1
        solution_type = "real"
    else:
        # Complex solutions
        real_part = -b / (2*a)
        imag_part = math.sqrt(abs(discriminant)) / (2*a)
        x1 = complex(real_part, imag_part)
        x2 = complex(real_part, -imag_part)
        solutions = [x1, x2]
        num_solutions = 2
        solution_type = "complex"
    
    return {
        "success": True,
        "equation": equation,
        "discriminant": discriminant,
        "num_solutions": num_solutions,
        "solution_type": solution_type,
        "solutions": solutions,
        "formatted_solutions": [_format_number(s) for s in solutions],
        "error": None
    }


def statistics(numbers: List[float]) -> Dict[str, Any]:
    """
    Calculate comprehensive statistics for a list of numbers.
    
    Args:
        numbers: A list of numeric values.
    
    Returns:
        A dictionary containing:
        - success: Whether the calculation succeeded
        - count: Number of values
        - sum: Sum of all values
        - mean: Arithmetic mean
        - median: Median value
        - mode: Most frequent value(s)
        - std_dev: Standard deviation
        - variance: Variance
        - min: Minimum value
        - max: Maximum value
        - range: Difference between max and min
        - quartiles: Q1, Q2 (median), Q3
        - error: Error message (if failed)
    
    Examples:
        >>> statistics([1, 2, 3, 4, 5])
        {'success': True, 'mean': 3.0, 'std_dev': 1.414..., ...}
    """
    if not numbers:
        return {
            "success": False,
            "error": "Empty list provided"
        }
    
    try:
        n = len(numbers)
        sorted_nums = sorted(numbers)
        total = sum(numbers)
        mean = total / n
        
        # Median
        if n % 2 == 0:
            median = (sorted_nums[n//2 - 1] + sorted_nums[n//2]) / 2
        else:
            median = sorted_nums[n//2]
        
        # Mode
        from collections import Counter
        counts = Counter(numbers)
        max_count = max(counts.values())
        modes = [k for k, v in counts.items() if v == max_count]
        mode = modes[0] if len(modes) == 1 else modes
        
        # Variance and Standard Deviation
        squared_diffs = [(x - mean) ** 2 for x in numbers]
        variance = sum(squared_diffs) / n
        std_dev = math.sqrt(variance)
        
        # Quartiles
        q1_idx = n // 4
        q3_idx = (3 * n) // 4
        q1 = sorted_nums[q1_idx]
        q3 = sorted_nums[q3_idx]
        
        return {
            "success": True,
            "count": n,
            "sum": total,
            "mean": mean,
            "median": median,
            "mode": mode,
            "std_dev": std_dev,
            "variance": variance,
            "min": min(numbers),
            "max": max(numbers),
            "range": max(numbers) - min(numbers),
            "quartiles": {"Q1": q1, "Q2": median, "Q3": q3},
            "iqr": q3 - q1,
            "error": None
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def _format_float(value: float, precision: int = 10) -> str:
    """Format a float value for display."""
    if value == int(value):
        return str(int(value))
    
    formatted = f"{value:.{precision}g}"
    return formatted


def _format_complex(value: complex) -> str:
    """Format a complex number for display."""
    real = value.real
    imag = value.imag
    
    if imag == 0:
        return _format_float(real)
    
    if real == 0:
        if imag == 1:
            return "i"
        elif imag == -1:
            return "-i"
        else:
            return f"{_format_float(imag)}i"
    
    sign = '+' if imag >= 0 else '-'
    imag_abs = abs(imag)
    
    if imag_abs == 1:
        return f"{_format_float(real)} {sign} i"
    else:
        return f"{_format_float(real)} {sign} {_format_float(imag_abs)}i"


def _format_number(value: Union[int, float, complex]) -> str:
    """Format any numeric value for display."""
    if isinstance(value, complex):
        return _format_complex(value)
    elif isinstance(value, float):
        return _format_float(value)
    else:
        return str(value)


# Tool metadata for LCP discovery
__tools__ = [
    {
        "name": "calculate",
        "description": "Evaluate any mathematical expression including arithmetic, algebra, trigonometry, logarithms, and more. Supports constants (pi, e), functions (sin, cos, log, sqrt), and complex numbers.",
        "function": calculate,
        "parameters": {
            "expression": {
                "type": "string",
                "description": "Mathematical expression to evaluate (e.g., '2 + 3*4', 'sqrt(16) + sin(pi/2)', 'factorial(10)')"
            }
        }
    },
    {
        "name": "calculate_with_steps",
        "description": "Evaluate a mathematical expression and show step-by-step calculation process.",
        "function": calculate_with_steps,
        "parameters": {
            "expression": {
                "type": "string",
                "description": "Mathematical expression to evaluate with steps"
            }
        }
    },
    {
        "name": "convert_units",
        "description": "Convert values between different units (length, mass, temperature, time, data, angle).",
        "function": convert_units,
        "parameters": {
            "value": {"type": "number", "description": "Value to convert"},
            "from_unit": {"type": "string", "description": "Source unit (e.g., 'km', 'lb', 'F')"},
            "to_unit": {"type": "string", "description": "Target unit (e.g., 'mi', 'kg', 'C')"}
        }
    },
    {
        "name": "solve_quadratic",
        "description": "Solve a quadratic equation ax² + bx + c = 0 and return all solutions (real or complex).",
        "function": solve_quadratic,
        "parameters": {
            "a": {"type": "number", "description": "Coefficient of x²"},
            "b": {"type": "number", "description": "Coefficient of x"},
            "c": {"type": "number", "description": "Constant term"}
        }
    },
    {
        "name": "statistics",
        "description": "Calculate comprehensive statistics (mean, median, mode, std dev, quartiles) for a list of numbers.",
        "function": statistics,
        "parameters": {
            "numbers": {"type": "array", "description": "List of numeric values"}
        }
    }
]