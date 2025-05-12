from langchain_openai import ChatOpenAI
from langchain_community.tools import TavilySearchResults
from langchain_core.messages import HumanMessage, AIMessage
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor
from langchain import hub
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory



search = TavilySearchResults(max_results=1)
tools = [search]

llm = ChatOpenAI(model="gpt-4o-mini")
prompt = hub.pull("hwchase17/openai-tools-agent")
agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

store = {}
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


agent_with_message_history = RunnableWithMessageHistory(
    agent_executor,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history"
)

agent_executor = agent_with_message_history.invoke(
    {
        "input": "我叫xuji",
    },
    config={
        "configurable": {
            "session_id": "123"
        }
    }
)


agent_executor = agent_with_message_history.invoke(
    {
        "input": "我叫什么名字？",
    },
    config={
        "configurable": {
            "session_id": "123"
        }
    }
)
print(agent_executor)