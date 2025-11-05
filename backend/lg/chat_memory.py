import sqlite3
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.prompts import SystemMessagePromptTemplate, ChatPromptTemplate
from typing import Literal
from langchain_core.messages import RemoveMessage, HumanMessage

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=GOOGLE_API_KEY,
    model_kwargs={"system_instruction": "You are assistant"},
)


class State(MessagesState):
    summary: str


summary_system_template = SystemMessagePromptTemplate.from_template(
    "Here is the existing conversation summary:\n{summary}\n\nRespond naturally to the next user message while maintaining the overall context."
)


def chat_node(state: State) -> State:
    summary = state.get("summary", "")
    if summary:
        prompt = ChatPromptTemplate.from_messages([summary_system_template])
        system_message = prompt.format_messages(summary=summary)[0]
        messages = [system_message] + state["messages"]
    else:
        messages = state["messages"]
    return {"messages": [llm.invoke(messages)], "summary": state.get("summary", "")}


def summary_node(state: State) -> State:
    summary = state.get("summary", "")
    if summary:
        summary_message = f"Previous summary:\n{summary}\n\nPlease update the summary to reflect the new messages above while keeping it concise."
    else:
        summary_message = "Create a concise summary of the above conversation:"
    messages = state["messages"] + [HumanMessage(content=summary_message)]
    response = llm.invoke(messages)
    delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]
    return {"summary": response.content, "messages": delete_messages}


def decide_node(state: State) -> Literal["summary_node", END]:
    if len(state["messages"]) > 5:
        return "summary_node"
    return END


db_path = "state_db/example.db"
os.makedirs(os.path.dirname(db_path), exist_ok=True)
conn = sqlite3.connect(db_path, check_same_thread=False)
memory = MemorySaver()

config = {"configurable": {"thread_id": "chat_1"}}
builder = StateGraph(State)

builder.add_node("chat_node", chat_node)
builder.add_node("summary_node", summary_node)

builder.add_edge(START, "chat_node")
builder.add_conditional_edges("chat_node", decide_node)
builder.add_edge("summary_node", END)

graph = builder.compile(checkpointer=memory)

# response = graph.invoke({"messages": [HumanMessage("Hello I'm Amit")]}, config=config)
# for m in response["messages"][-1:]:
#     m.pretty_print()

# response = graph.invoke({"messages": [HumanMessage("I like cricket")]}, config=config)
# for m in response["messages"][-1:]:
#     m.pretty_print()

# response = graph.invoke({"messages": [HumanMessage("I like MS Dhoni")]}, config=config)
# for m in response["messages"][-1:]:
#     m.pretty_print()

response = graph.invoke(
    {"messages": [HumanMessage("Tell me about Amit")]}, config=config
)
for m in response["messages"][-1:]:
    m.pretty_print()

state = graph.get_state(config)
print(state)
