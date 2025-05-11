from langchain_core.tools import StructuredTool
from langchain_core.tools import ToolException

def get_weather(city: str) -> str:
    """Get the weather in a given city"""
    raise ToolException(f"{city} not found")

def _handle_error(error: ToolException) -> str:
    return f"工具执行期间发生如下错误: {error.args[0]}"

get_weather_tool =StructuredTool.from_function(
    func=get_weather,
    handle_tool_error=_handle_error
)

response = get_weather_tool.invoke({"city": "Beijing"})
print(response)


