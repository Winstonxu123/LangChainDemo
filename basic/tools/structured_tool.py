from langchain.tools import StructuredTool
import asyncio

def multiply(a: int, b: int) -> int:
    """Multiply two integers"""
    return a * b

async def multiply_async(a: int, b: int) -> int:
    """Multiply two integers asynchronously"""
    return a * b

async def main():
    # func 参数：指定同步函数
    # coroutine 参数：指定一个异步函数
    calculator = StructuredTool.from_function(func=multiply, coroutine=multiply_async)
    print(calculator.invoke({"a": 2, "b": 3}))
    print(await calculator.ainvoke({"a": 2, "b": 5}))

asyncio.run(main())
