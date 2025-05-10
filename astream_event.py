from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
import asyncio
model = ChatOpenAI(model="gpt-3.5-turbo")

async def async_stream():
    events = []
    async for event in model.astream_events("hello"):
        events.append(event)
    print(events)
    
asyncio.run(async_stream())