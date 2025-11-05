from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
from langchain.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict, Annotated
from langchain.schema.messages import HumanMessage

# ------------------- Setup -------------------
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=GOOGLE_API_KEY,
    model_kwargs={"system_instruction": "You are a helpful assistant..."},
)


# ------------------- Tools -------------------
@tool
def add(a, b):
    """Add two numbers"""
    return a + b


@tool
def multiply(a, b):
    """Multiply two numbers"""
    return a * b


tools = [add, multiply]
llm_with_tools = llm.bind_tools(tools)


# ------------------- Agent State -------------------
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


# ------------------- Node Logic -------------------
def tool_calling_llm(state: AgentState) -> AgentState:
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": state["messages"] + [response]}


# ------------------- Graph Building -------------------
memory = MemorySaver()
builder = StateGraph(AgentState)
builder.add_node("tool_calling_llm", tool_calling_llm)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "tool_calling_llm")
builder.add_conditional_edges("tool_calling_llm", tools_condition)
builder.add_edge("tools", "tool_calling_llm")

graph = builder.compile()

config = {"configurable": {"thread_id": "uniq_"}}

response = graph.invoke({"messages": [HumanMessage("Hello, I'm Amit.")]}, config=config)
print(response["messages"][-1].content)


response = graph.invoke({"messages": [HumanMessage("What is my name?")]}, config=config)
print(response["messages"][-1].content)
