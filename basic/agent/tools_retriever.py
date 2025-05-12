from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.tools import create_retriever_tool

loader = WebBaseLoader("https://zh.wikipedia.org/wiki/%E7%8C%AB")
docs = loader.load()
documents = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=200
).split_documents(docs)

embeddings = OpenAIEmbeddings()
vector = FAISS.from_documents(documents, embeddings)
retriever = vector.as_retriever()

response = retriever.invoke("猫科动物有哪些特征？")
print(response)

retriever_tool = create_retriever_tool(
    retriever=retriever,
    name="wikipedia",
    description="Search Wikipedia for information"
)

