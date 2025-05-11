from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from pydantic import BaseModel, Field

class WikipediaQuery(BaseModel):
    query: str = Field(..., description="query to look up in Wikipedia, should be 3 or less words")

api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)
tool = WikipediaQueryRun(
    name="wikipedia",
    api_wrapper=api_wrapper,
    description="Search Wikipedia for information",
    args_schema=WikipediaQuery,
    # 如果设置为 True，则将返回原始结果，而不是将结果作为响应
    return_direct=True
)
print(tool.invoke({"query": "LangChain"}))
