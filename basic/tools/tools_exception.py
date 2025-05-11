from langchain_core.tools import StructuredTool
from langchain_core.tools import ToolException

def get_weather(city: str) -> str:
    """Get the weather in a given city"""
    raise ToolException(f"{city} not found")


get_weather_tool =StructuredTool.from_function(
    func=get_weather, 
    # 默认情况下，如果函数抛出 ToolException，则将 ToolException 的 message 作为响应
    # 如果设置为 True，则将返回 ToolException 异常文本，False 将会抛出 ToolException                    
    handle_tool_error=True
)

response = get_weather_tool.invoke({"city": "Beijing"})
print(response)


