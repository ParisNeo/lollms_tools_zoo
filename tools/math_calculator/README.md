# Math Calculator Toolset

Mathematical operations, statistics, and calculations for the LCP framework.

## Overview

This toolset provides a comprehensive set of mathematical operations ranging from basic arithmetic to statistical analysis. All operations are type-safe and include proper error handling.

## Tools

### Basic Arithmetic

#### `tool_add`
Adds two numbers.

**Parameters:**
- `a` (float): First number
- `b` (float): Second number

**Returns:** Dictionary with result.

---

#### `tool_subtract`
Subtracts two numbers.

**Parameters:**
- `a` (float): First number
- `b` (float): Second number

**Returns:** Dictionary with result.

---

#### `tool_multiply`
Multiplies two numbers.

**Parameters:**
- `a` (float): First number
- `b` (float): Second number

**Returns:** Dictionary with result.

---

#### `tool_divide`
Divides two numbers with zero-division protection.

**Parameters:**
- `a` (float): Numerator
- `b` (float): Denominator

**Returns:** Dictionary with result or error if dividing by zero.

---

### Advanced Operations

#### `tool_power`
Raises a number to a power.

**Parameters:**
- `base` (float): Base number
- `exponent` (float): Exponent

**Returns:** Dictionary with result.

---

#### `tool_square_root`
Calculates square root with negative number protection.

**Parameters:**
- `number` (float): Input number

**Returns:** Dictionary with result or error for negative inputs.

---

#### `tool_factorial`
Calculates factorial of a non-negative integer.

**Parameters:**
- `n` (int): Non-negative integer

**Returns:** Dictionary with result or error for negative inputs.

---

### Statistical Operations

#### `tool_calculate_mean`
Calculates arithmetic mean of a list.

**Parameters:**
- `numbers` (List[float]): List of numbers

**Returns:** Dictionary with mean, sum, and count.

---

#### `tool_calculate_median`
Calculates median of a list.

**Parameters:**
- `numbers` (List[float]): List of numbers

**Returns:** Dictionary with median and count.

---

#### `tool_calculate_std_dev`
Calculates standard deviation (sample).

**Parameters:**
- `numbers` (List[float]): List of numbers (minimum 2)

**Returns:** Dictionary with standard deviation, variance, mean, and count.

---

#### `tool_calculate_percentage`
Calculates what percentage a part is of a whole.

**Parameters:**
- `part` (float): Part value
- `whole` (float): Whole value

**Returns:** Dictionary with percentage or error if whole is zero.

## Usage Examples

```python
# Basic arithmetic
tool_add(a=15.5, b=24.3)
tool_divide(a=100, b=4)

# Advanced operations
tool_power(base=2, exponent=10)
tool_square_root(number=144)
tool_factorial(n=5)

# Statistics
data = [12, 15, 18, 22, 25, 28, 30]
tool_calculate_mean(numbers=data)
tool_calculate_median(numbers=data)
tool_calculate_std_dev(numbers=data)

# Percentage
tool_calculate_percentage(part=25, whole=200)
```

## Error Handling

- **Division by Zero**: Returns error dictionary
- **Negative Square Root**: Returns error dictionary
- **Negative Factorial**: Returns error dictionary
- **Empty Lists**: Statistical functions return error for empty inputs
- **Insufficient Data**: Standard deviation requires at least 2 values

## Type Safety

All functions use proper type hints and validate input types. Float and integer operations are handled appropriately.