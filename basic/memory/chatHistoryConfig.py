from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.prompts import HumanMessagePromptTemplate

from langchain_core.runnables import ConfigurableFieldSpec


prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant who's good at {ability}. Respond in 20 words or less."),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}"),
])

model = ChatOpenAI()
runnable = prompt | model
store = {}

def get_session_history(use_id: str, conversation_id: str) -> BaseChatMessageHistory:
    if (use_id, conversation_id) not in store:
        store[(use_id, conversation_id)] = ChatMessageHistory()
    return store[(use_id, conversation_id)]

with_message_history = RunnableWithMessageHistory(
    runnable, 
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
    history_factory_config=[
        ConfigurableFieldSpec(
            id="use_id",
            annotation=str,
            name="user id",
            description="The id of the user",
            default="",
            is_shared=True
        ),
        ConfigurableFieldSpec(
            id="conversation_id",
            annotation=str,
            name="conversation id",
            description="The id of the conversation",
            default="",
            is_shared=True
        )
    ]
)

response = with_message_history.invoke(
    input={"ability": "math", "input": "余弦函数是什么意思？"}, 
    config={"configurable": {"use_id": "123", "conversation_id": "456"}}
)

print(response)