from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")


def llm_calling(state: MessagesState):
    result = llm.invoke(state["messages"])
    return {"messages": [("assistant", result.content)]}


memory = MemorySaver()

builder = StateGraph(MessagesState)
builder.add_node("llm", llm_calling)
builder.add_edge(START, "llm")
builder.add_edge("llm", END)

graph = builder.compile(checkpointer=memory)

# config = {"configurable": {"thread_id": "chat_1"}}
# response = graph.invoke({"messages": [("human", "Hello, I'm Amit")]}, config=config)
# print(response["messages"][-1].pretty_print())
# response = graph.invoke(
#     {"messages": [("human", "What do you know about me so far ?")]},
#     config=config,
# )
# print(response["messages"][-1].pretty_print())


# to be used in flask endpoint
def ask_text_model(user_input: str, session_id: str = "default"):
    config = {"configurable": {"thread_id": session_id}}
    response = graph.invoke({"messages": [("human", user_input)]}, config=config)
    return response["messages"][-1].content
