from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from models import gemini_llm

# --- Session store ---
session_histories = {}


def get_session_history(session_id: str):
    if session_id not in session_histories:
        session_histories[session_id] = ChatMessageHistory()
    return session_histories[session_id]


# --- Chain setup ---
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)
base_chain = prompt_template | gemini_llm

chain = RunnableWithMessageHistory(
    base_chain,
    get_session_history=get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)


# --- Usage ---
def ask_text_model(user_input: str, session_id: str = "default"):
    response = chain.invoke(
        {"input": user_input},
        config={"configurable": {"session_id": session_id}},
    )
    return response.content
