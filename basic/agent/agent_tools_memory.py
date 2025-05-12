from langchain.agents import create_tool_calling_agent
from langchain_community.tools import TavilySearchResults
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain_core.messages import HumanMessage, AIMessage


search = TavilySearchResults(max_results=1)
tools = [search]

prompt = hub.pull("hwchase17/openai-tools-agent")

llm = ChatOpenAI(model="gpt-4o-mini")
from langchain.agents import AgentExecutor
agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
response = agent_executor.invoke(
    {
        "input": "我叫什么名字?",
        "chat_history": [
            HumanMessage(content="hi! my name is bob"),
            AIMessage(content="你好Bob！我今天能帮你什么？"),
        ]
    }
)
print(response)