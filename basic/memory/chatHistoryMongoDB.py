from langchain_mongodb import MongoDBChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain.prompts import HumanMessagePromptTemplate
from langchain_deepseek import ChatDeepSeek


prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant who's good at {ability}. Respond in 20 words or less."),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}"),
])

model = ChatDeepSeek(model="deepseek-chat")
runnable = prompt | model

store = {}

MONGO_URI = "mongodb://localhost:27017"

def get_message_history(session_id: str) -> MongoDBChatMessageHistory:
    return MongoDBChatMessageHistory(
        session_id=session_id, 
        connection_string=MONGO_URI,
        database_name="chat_memory_db",
        collection_name="chat_messages",
        create_index=True
    )

with_message_history = RunnableWithMessageHistory(
    runnable,
    get_message_history,
    input_messages_key="input",
    history_messages_key="history",
)

response = with_message_history.invoke(
    input={"ability": "math", "input": "余弦函数是什么意思？"}, 
    config={"configurable": {"session_id": "123"}}
)
print(response)    
