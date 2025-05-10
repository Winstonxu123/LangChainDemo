# 引入 langchain 提示词模版
from langchain_core.prompts import ChatPromptTemplate
# 引入 langchain 的 openai sdk
from langchain_openai import ChatOpenAI

from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI()

# 根据 message 生成提示词模版
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是世界级的技术专家"),
    ("user", "{input}")
])

output_parser = StrOutputParser()

# 通过 langchain 的链式调用，生成一个 chain
chain = prompt | llm | output_parser

result = chain.invoke({"input": "你的知识截止到什么时候"})
print(result)