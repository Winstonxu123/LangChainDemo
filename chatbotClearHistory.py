from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_deepseek import ChatDeepSeek
from langchain_core.runnables import RunnablePassthrough
from langchain.prompts import HumanMessagePromptTemplate

temp_chat_history = ChatMessageHistory()
temp_chat_history.add_user_message("I am jack, hello")
temp_chat_history.add_ai_message("hello, jack")
temp_chat_history.add_user_message("I feel good")
temp_chat_history.add_ai_message("I feel good too")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}"),
])

model = ChatDeepSeek(model="deepseek-chat")

chain = prompt | model

def trim_messages(chain_input):
    stored_messages = temp_chat_history.messages
    if len(stored_messages) <= 4:
        return False;
    temp_chat_history.clear()
    for message in stored_messages[-4:]:
        temp_chat_history.add_message(message)
    return True

chain_with_message_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: temp_chat_history,
    input_messages_key="input",
    history_messages_key="history",
)

chain_with_message_trim = (
    RunnablePassthrough.assign(history=trim_messages) | chain_with_message_history
)

response = chain_with_message_trim.invoke(
    input={"input": "我叫什么名字?"},
    config={"configurable": {"session_id": "unused"}}
)

print(response)