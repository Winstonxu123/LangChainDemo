#!/usr/bin/env python
from fastapi import FastAPI
from langchain_openai import ChatOpenAI
from langserve import add_routes
app = FastAPI(
    title="LangChain 服务器",
    version="1.0",
    description="使用 Langchain 的 Runnable 接口的简单 API 服务器",
)
add_routes(
    app,
    ChatOpenAI(),
    path="/openai",
)

from langchain_core.output_parsers import StrOutputParser
parser = StrOutputParser()
add_routes(
    app,
    ChatOpenAI() | parser,
    path="/openai_str_parser",
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)