from langchain.tools import StructuredTool
from pydantic import BaseModel, Field
import asyncio
class CalculatorInput(BaseModel):
    a: int = Field(description="第一个整数")
    b: int = Field(description="第二个整数")

def multiply(a: int, b: int) -> int:
    """Multiply two integers"""
    return a * b

async def async_addition(a: int, b: int) -> int:
    """Add two integers"""
    return a + b


async def main():
    calculator = StructuredTool.from_function(
        func=multiply,
        name="calculator",
        description="multiply numbers",
        args_schema=CalculatorInput,
        return_direct=True
    )
    print(calculator.invoke({"a": 2, "b": 3}))
    print(calculator.name)
    print(calculator.description)
    print(calculator.args_schema)
    print(calculator.return_direct)

asyncio.run(main())

