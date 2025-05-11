from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
import asyncio

model = ChatOpenAI(model="gpt-3.5-turbo")

prompt = ChatPromptTemplate.from_template("给我讲一个{topic}的笑话")
parser = StrOutputParser()
chain = (model | JsonOutputParser())

async def inner():
    async for chunk in chain.astream("以JSON 格式输出法国、西班牙和日本的国家及其人口列表。"
        '使用一个带有“countries”外部键的字典，其中包含国家列表。'
        "每个国家都应该有键`name`和`population`"):
        print(chunk, flush=True)
    
asyncio.run(inner())

