def binary_operation(x: str, y: str, operator: str) -> str:
    a = int(x, 2)
    b = int(y, 2)

    if operator == '+':
        result = a + b
    elif operator == '-':
        result = a - b
    elif operator == '*':
        result = a * b
    elif operator == '/':
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        result = a // b
    elif operator == '<<':
        result = a << b
    elif operator == '>>':
        result = a >> b
    else:
        raise ValueError(f"Unsupported operator: {operator}")

    return bin(result if result >= 0 else (1 << 32) + result)[2:]

#print(binary_operation("11011", "10101", "+"))

