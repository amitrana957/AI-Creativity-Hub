from typing import TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=GOOGLE_API_KEY)


class ReState(TypedDict):
    val: int


def node1(state: ReState) -> ReState:
    return {"val": state["val"] + 1}


def node2(state: ReState) -> ReState:
    return {"val": state["val"] + 1}


def node3(state: ReState) -> ReState:
    return {"val": state["val"] + 1}


graph = StateGraph(ReState)
graph.add_node("node1", node1)
graph.add_node("node2", node2)
graph.add_node("node3", node3)

graph.add_edge(START, "node1")

graph.add_edge("node1", "node2")
graph.add_edge("node1", "node3")

graph.add_edge("node2", END)
graph.add_edge("node3", END)

app = graph.compile()

app.invoke({"val": 0})
