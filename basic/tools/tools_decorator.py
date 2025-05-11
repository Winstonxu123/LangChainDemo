from langchain_core.tools import tool

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers"""
    return a * b

print(multiply.name)
print(multiply.description)
print(multiply.args)





