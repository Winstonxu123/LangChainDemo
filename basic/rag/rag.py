# 使用 streamlit run basic/rag/rag.py 运行
import streamlit as st

# 上传txt文件，允许上传多个文件
uploaded_files = st.sidebar.file_uploader(
    label="上传txt文件", 
    type=["txt"], 
    accept_multiple_files=True
)
if not uploaded_files:
    st.info("请上传txt文件")
    st.stop()


import tempfile
import os
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.memory import ConversationBufferMemory   
from langchain.memory import StreamlitChatMessageHistory

# 实现检索器
@st.cache_resource(ttl="1h")
def configure_retriever(uploaded_files):
    # 读取上传的文档，并写入一个临时目录
    docs = []
    temp_dir = tempfile.TemporaryDirectory(dir=r"/Users/xuji")
    for file in uploaded_files:
        temp_file_path = os.path.join(temp_dir.name, file.name)
        with open(temp_file_path, "wb") as f:
            f.write(file.getvalue())
        loader = TextLoader(temp_file_path, encoding="utf-8")
        docs.extend(loader.load())
    
    # 进行文档分割
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    
    # 这里使用了OpenAI向量模型
    embeddings = OpenAIEmbeddings()
    vectordb= Chroma.from_documents(splits, embeddings)
    retriever = vectordb.as_retriever()
    return retriever

retriever = configure_retriever(uploaded_files)

# 清空聊天记录
if "messages" not in st.session_state or st.sidebar.button("清空聊天记录"):
    st.session_state["messages"] = [{"role": "assistant", "content": "您好，我是您的私人助理，有什么可以帮您的吗？"}]

# 加载历史聊天记录
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 创建检索工具
from langchain.tools.retriever import create_retriever_tool

rag_tool = create_retriever_tool(
    retriever,
    "文档检索",
    "用于检索用户提出的问题，并基于检索到的文档内容进行回复"
)

tools = [rag_tool]

# 创建聊天消息历史记录
msgs = StreamlitChatMessageHistory()
# 创建对话缓冲区内存
memory = ConversationBufferMemory(chat_memory=msgs, 
                                  return_messages=True,
                                  memory_key="chat_history",
                                  output_key="output")

instructions = """您是一个设计用于查询文档来回答问题的代理。
您可以使用文档检索工具，并基于检索内容来回答问题
您可能不查询文档就知道答案，但是您仍然应该查询文档来获得答案。
如果您从文档中找不到任何信息用于回答问题，则只需返回“抱歉，这个问题我还不知道。”作为答案。
"""

base_prompt_template = """
{instructions}

TOOLS:
------

You have access to the following tools:

{tools}

To use a tool, please use the following format:

•```
Thought: Do I need to use a tool? Yes
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
•```

When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:

•```
Thought: Do I need to use a tool? No
Final Answer: [your response here]
•```

Begin!

Previous conversation history:
{chat_history}

New input: {input}
{agent_scratchpad}"""

from langchain.prompts import PromptTemplate
from langchain.agents import create_react_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain.callbacks import StreamlitCallbackHandler
base_prompt = PromptTemplate.from_template(base_prompt_template)
prompt = base_prompt.partial(instructions=instructions)
# 创建llm
llm = ChatOpenAI()

# 创建react Agent
agent = create_react_agent(llm, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, memory=memory, verbose=False)

# 创建聊天输入框
user_query = st.chat_input(placeholder="请开始提问吧!")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container())
        config = {"callbacks": [st_cb]}
        response = agent_executor.invoke({"input": user_query}, config=config)
        st.session_state.messages.append({"role": "assistant", "content": response["output"]})
        st.write(response["output"])





