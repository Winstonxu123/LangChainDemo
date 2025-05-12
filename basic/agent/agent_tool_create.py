from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.tools import create_retriever_tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI

loader = WebBaseLoader("https://zh.wikipedia.org/wiki/%E7%8C%AB")
docs = loader.load()
documents = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=200
).split_documents(docs)

# embeddings = OpenAIEmbeddings()
# vector = FAISS.from_documents(documents, embeddings)
# retriever = vector.as_retriever()

# response = retriever.invoke("猫科动物有哪些特征？")
# print(response)

# retriever_tool = create_retriever_tool(
#     retriever=retriever,
#     name="wikipedia",
#     description="Search Wikipedia for information"
# )

search = TavilySearchResults(max_results=1)

tools = [search,
         #retriever_tool
]

from langchain import hub
from langchain.agents import create_tool_calling_agent

prompt = hub.pull("hwchase17/openai-tools-agent")

llm = ChatOpenAI(model="gpt-4o-mini")
agent = create_tool_calling_agent(llm, tools, prompt)

from langchain.agents import AgentExecutor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
print(agent_executor.invoke({"input": "上海天气怎么样？"}))