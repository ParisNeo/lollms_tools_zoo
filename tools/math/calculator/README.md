# Universal Math Calculator Toolset

A powerful, safe mathematical expression evaluator that handles complex formulas including arithmetic, algebra, trigonometry, logarithms, unit conversions, quadratic equations, and statistics. Uses AST parsing for safe evaluation without exec/eval.

## Features

- **Safe Expression Evaluation**: AST-based parsing prevents arbitrary code execution
- **Rich Mathematical Functions**: Trigonometry, logarithms, exponentials, hyperbolic functions
- **Complex Number Support**: Full support for imaginary and complex arithmetic
- **Unit Conversion**: Convert between length, mass, temperature, time, data, and angle units
- **Quadratic Solver**: Solve ax² + bx + c = 0 with real and complex solutions
- **Statistics**: Comprehensive statistical analysis (mean, median, mode, std dev, quartiles)
- **Step-by-Step Solutions**: Educational breakdown of calculation steps

## Tools

### `calculate(expression: str) -> dict`

Evaluates a mathematical expression safely.

**Parameters:**
- `expression` (str): Mathematical expression to evaluate

**Returns:**
- `dict`: Result dictionary containing:
  - `success`: Boolean indicating success
  - `expression`: The original expression
  - `result`: The computed result
  - `result_type`: Type of result (integer, float, complex, sequence)
  - `formatted`: Human-readable formatted result
  - `error`: Error message if failed

**Supported Operations:**
- Arithmetic: `+`, `-`, `*`, `/`, `//`, `%`, `^` or `**`
- Implicit multiplication: `2(3)` = 6
- Percentages: `50%` = 0.5
- Parentheses for grouping

**Supported Functions:**
- Basic: `abs`, `round`, `floor`, `ceil`, `trunc`
- Power/Roots: `sqrt`, `cbrt`, `pow`, `exp`, `expm1`
- Logarithms: `log`, `ln`, `log10`, `log2`, `log1p`
- Trigonometric: `sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `atan2`
- Degree-based: `sind`, `cosd`, `tand`, `asind`, `acosd`, `atand`, `atan2d`
- Hyperbolic: `sinh`, `cosh`, `tanh`, `asinh`, `acosh`, `atanh`
- Special: `factorial`, `gamma`, `lgamma`, `erf`, `erfc`
- Combinatorics: `comb`, `perm`, `gcd`, `lcm`
- Geometry: `hypot`, `dist`
- Complex: `real`, `imag`, `conj`, `phase`, `abs_complex`
- Utility: `min`, `max`, `sum`, `sign`, `clamp`

**Constants:**
- `pi`: π (3.14159...)
- `e`: Euler's number (2.71828...)
- `tau`: τ (2π)
- `inf`: Infinity
- `i`, `j`: Imaginary unit

**Examples:**
```python
calculate("2 + 3 * 4")                    # Returns 14
calculate("sqrt(16) + sin(pi/2)")         # Returns 5.0
calculate("factorial(10) / comb(10, 3)")  # Returns 30240.0
calculate("abs(3+4j)")                    # Returns 5.0
calculate("50% of 200")                   # Returns 100.0
```

---

### `calculate_with_steps(expression: str) -> dict`

Evaluates an expression and returns detailed calculation steps.

**Parameters:**
- `expression` (str): Mathematical expression to evaluate

**Returns:**
- `dict`: Result dictionary containing:
  - `success`: Boolean indicating success
  - `expression`: The original expression
  - `result`: The computed result
  - `steps`: List of calculation steps
  - `error`: Error message if failed

**Example:**
```python
calculate_with_steps("2 + 3 * 4")
# Returns: {
#   'success': True,
#   'steps': ['3 * 4 = 12', '2 + 12 = 14'],
#   'result': 14
# }
```

---

### `convert_units(value: float, from_unit: str, to_unit: str) -> dict`

Converts a value between different units of measurement.

**Parameters:**
- `value` (float): The numeric value to convert
- `from_unit` (str): Source unit
- `to_unit` (str): Target unit

**Supported Units:**

| Category | Units |
|----------|-------|
| Length | `mm`, `cm`, `m`, `km`, `in`, `ft`, `yd`, `mi` |
| Mass | `mg`, `g`, `kg`, `t`, `oz`, `lb` |
| Temperature | `C`, `F`, `K` |
| Time | `ms`, `s`, `min`, `hr`, `day`, `week`, `year` |
| Data | `B`, `KB`, `MB`, `GB`, `TB` |
| Angle | `deg`, `rad`, `grad` |

**Returns:**
- `dict`: Result dictionary containing:
  - `success`: Boolean indicating success
  - `original_value`: Input value
  - `original_unit`: Source unit
  - `converted_value`: Converted value
  - `converted_unit`: Target unit
  - `formatted`: Human-readable result
  - `error`: Error message if failed

**Examples:**
```python
convert_units(100, 'km', 'mi')   # Returns 62.137...
convert_units(32, 'F', 'C')      # Returns 0.0
convert_units(1, 'GB', 'MB')     # Returns 1024.0
```

---

### `solve_quadratic(a: float, b: float, c: float) -> dict`

Solves a quadratic equation ax² + bx + c = 0.

**Parameters:**
- `a` (float): Coefficient of x²
- `b` (float): Coefficient of x
- `c` (float): Constant term

**Returns:**
- `dict`: Result dictionary containing:
  - `success`: Boolean indicating success
  - `equation`: Formatted equation string
  - `discriminant`: The discriminant (b² - 4ac)
  - `num_solutions`: Number of solutions (0, 1, or 2)
  - `solution_type`: "real" or "complex"
  - `solutions`: List of solutions
  - `formatted_solutions`: Human-readable solutions
  - `error`: Error message if failed

**Examples:**
```python
solve_quadratic(1, -5, 6)   # x² - 5x + 6 = 0 → solutions: [3.0, 2.0]
solve_quadratic(1, 0, 1)    # x² + 1 = 0 → solutions: [1j, -1j]
solve_quadratic(1, 2, 1)    # x² + 2x + 1 = 0 → solutions: [-1.0]
```

---

### `statistics(numbers: list) -> dict`

Calculates comprehensive statistics for a list of numbers.

**Parameters:**
- `numbers` (list): List of numeric values

**Returns:**
- `dict`: Result dictionary containing:
  - `success`: Boolean indicating success
  - `count`: Number of values
  - `sum`: Sum of all values
  - `mean`: Arithmetic mean
  - `median`: Median value
  - `mode`: Most frequent value(s)
  - `std_dev`: Standard deviation
  - `variance`: Variance
  - `min`: Minimum value
  - `max`: Maximum value
  - `range`: Difference between max and min
  - `quartiles`: Q1, Q2 (median), Q3
  - `iqr`: Interquartile range
  - `error`: Error message if failed

**Example:**
```python
statistics([1, 2, 3, 4, 5])
# Returns: {
#   'success': True,
#   'count': 5,
#   'sum': 15,
#   'mean': 3.0,
#   'median': 3,
#   'std_dev': 1.414...,
#   ...
# }
```

## Error Handling

All tools return a dictionary with a `success` field. If `success` is `False`, the `error` field contains a description of what went wrong.

Common errors:
- `"Division by zero"`: Attempted to divide by zero
- `"Unknown function: X"`: Function not in supported list
- `"Unknown variable: X"`: Variable not defined
- `"Math domain error"`: Invalid input for function (e.g., `sqrt(-1)`)
- `"Invalid syntax"`: Expression cannot be parsed

## LCP Integration

This toolset follows the LCP (LollmsCommunicationProtocol) requirements:

- **`init_tools_library()`**: Lazy initialization function called on first tool invocation
- **Health Gate**: Returns `True` if initialization succeeds, `False` otherwise
- **AST Discovery**: Tools are discovered via AST parsing without module execution

## Dependencies

- Python 3.8+
- No external dependencies (uses only standard library: `ast`, `math`, `operator`, `re`)

## Security

- Uses AST parsing to safely evaluate expressions
- No `exec()` or `eval()` calls
- Blocks access to private names (starting with `_`)
- Validates all operations against whitelist