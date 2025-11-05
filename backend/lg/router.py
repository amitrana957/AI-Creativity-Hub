from chain import tool_calling_llm, multiply
from langgraph.graph import START, END, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langchain.schema.messages import HumanMessage

graph = StateGraph(MessagesState)
graph.add_node("tool_calling_llm", tool_calling_llm)
graph.add_node("tools", ToolNode([multiply]))
graph.add_edge(START, "tool_calling_llm")
graph.add_conditional_edges("tool_calling_llm", tools_condition)
graph.add_edge("tools", END)
app = graph.compile()


messages = app.invoke({"messages": HumanMessage("Multiply 5959 and 70")})

for m in messages["messages"]:
    m.pretty_print()
