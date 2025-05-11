from langchain_core.tools import tool

@tool
async def multiply(a: int, b: int) -> int:
    """Multiply two integers"""
    return a * b

print(multiply.name)
print(multiply.description)
print(multiply.args)

from pydantic import BaseModel, Field
class CalculatorInput(BaseModel):
    a: int = Field(description="第一个整数")
    b: int = Field(description="第二个整数")

@tool("multiplication-tool", args_schema=CalculatorInput, return_direct=True)
async def multiply2(a: int, b: int) -> int:
    """Multiply two integers"""
    return a * b

# 让我们检查与该工具关联的一些属性。
print(multiply2.name)
print(multiply2.description)
print(multiply2.args)
print(multiply2.return_direct)