from langchain.schema.messages import AIMessage, HumanMessage, AnyMessage
from pprint import pprint
from models import gemini_llm as llm
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain.tools import tool


@tool
def multiply(a, b):
    """Multiply two numbers"""
    return a * b


llm_with_tools = llm.bind_tools([multiply])


def tool_calling_llm(state: MessagesState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


graph = StateGraph(MessagesState)
graph.add_node("tool_calling_llm", tool_calling_llm)
graph.add_edge(START, "tool_calling_llm")
graph.add_edge("tool_calling_llm", END)
app = graph.compile()
