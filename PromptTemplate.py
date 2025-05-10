from langchain_core.prompts import ChatPromptTemplate

# 通过一个消息数组创建聊天消息模板
# 数组每一个元素代表一条消息，每个消息元组，第一个元素代表消息角色（也成为消息类型），第二个元素代表消息内容。
# 消息角色：system代表系统消息、human代表人类消息，ai代表LLM返回的消息内容
# 下面消息定义了2个模板参数name和user_input
chat_template = ChatPromptTemplate.from_messages([
    ("system", "你是一位人工智能助手，你的名字是{name}。"),
    ("human", "你好"),
    ("ai", "我很好，谢谢！"),
    ("human", "{user_input}")
])

messages = chat_template.format_messages(name="Bob", user_input="你的名字叫什么")
print(messages)


from langchain.prompts import HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate

chat_template = ChatPromptTemplate.from_messages([
    SystemMessage(content="你是一个乐于助人的助手，可以润色内容，使其看起来起来更简单易读。"),
    HumanMessagePromptTemplate.from_template("{text}"),
])

# 使用模板参数格式化模板
messages = chat_template.format_messages(text="我不喜欢吃好吃的东西")
print(messages)

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant"),
    MessagesPlaceholder("msgs"),
])

prompt_template.invoke({"msgs": [HumanMessage(content="hi!")]})