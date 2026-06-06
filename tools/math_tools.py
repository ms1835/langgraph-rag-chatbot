from langchain_core.tools import tool

@tool
def add(a: float, b: float) -> float:
    """Perform addition on given two numbers.
    
    Args:
        a: First number to add
        b: Second number to add
        
    Returns:
        The sum of a and b
    """
    return a + b


@tool
def subtract(a: float, b: float) -> float:
    """Perform subtraction on given two numbers.
    
    Args:
        a: First number to subtract from
        b: Second number to subtract
        
        
    Returns:
        The difference of a and b
    """
    return a - b

@tool
def multiply(a: float, b: float) -> float:
    """Perform multiplication on given two numbers.

    Args:
        a: First number to multiply
        b: Second number to multiply

    Returns:
        The product of a and b
    """
    return a * b

@tool
def divide(a: float, b: float) -> float:
    """Perform division on given two numbers.

    Args:
        a: First number to divide
        b: Second number to divide

    Returns:
        The quotient of a and b
    """
    if b == 0:
        raise ValueError("Second number cannot be zero.")
    return a / b

@tool
def square(a: float) -> float:
    """Calculate the square of a number.

    Args:
        a: The number to be squared

    Returns:
        The square of a
    """
    return a * a

@tool
def modulo(a: float, b: float) -> float:
    """Perform modulo operation on given two numbers.

    Args:
        a: First number to perform modulo on
        b: Second number to perform modulo with

    Returns:
        The result of a modulo b
    """
    if b == 0:
        raise ValueError("Second number cannot be zero.")
    return a % b

@tool
def parse_expression(expression: str) -> str:
    """
    Parse a mathematical expression and return an ordered list of steps to
    solve it following BODMAS rule:
    Brackets -> Orders (powers) -> Division -> Multiplication ->
    Addition -> Subtraction.
    Returns a human readable step-by-step plan.
    """
    expr = expression.replace("^", "**").replace("×", "*").replace("÷", "/")

    try:
        result = eval(expr)
    except Exception as e:
        return f"Invalid expression: {e}"

    steps = []
    steps.append(f"Expression: {expression}")
    steps.append(f"Normalized: {expr}")
    steps.append("")
    steps.append("BODMAS breakdown:")
    steps.append("  B - Brackets: resolve innermost parentheses first")
    steps.append("  O - Orders: handle powers/exponents (** or ^)")
    steps.append("  D - Division: left to right")
    steps.append("  M - Multiplication: left to right")
    steps.append("  A - Addition: left to right")
    steps.append("  S - Subtraction: left to right")
    steps.append("")
    steps.append(f"Final answer: {result}")
    steps.append("Now use the individual arithmetic tools to verify each step.")
    return "\n".join(steps)