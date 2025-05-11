from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field


model = ChatOpenAI()

# 定义期望的数据结构
class Joke(BaseModel):
    setup: str = Field(description="设置笑话的问题")
    punchline: str = Field(description="解决笑话的答案")



joke_query = "告诉我一个笑话"
parser = JsonOutputParser(pydantic_object=Joke)

prompt = PromptTemplate(
    template="""
    回答用户的查询。\n{format_instructions}\n{query}\n
    """,
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

chain = prompt | model | parser


for s in chain.stream({"query": joke_query}):
    print(s)