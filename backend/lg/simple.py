from langgraph.graph import START, END, StateGraph
from IPython.display import display, Image
import random
from typing import Literal, TypedDict


class SimpleState(TypedDict):
    graph_state: str


def node1(state: SimpleState) -> SimpleState:
    print("-- Node1 --")
    return {"graph_state": state["graph_state"] + " I'm"}


def node2(state: SimpleState) -> SimpleState:
    print("-- Node2 --")
    return {"graph_state": state["graph_state"] + " happy!!"}


def node3(state: SimpleState) -> SimpleState:
    print("-- Node3 --")
    return {"graph_state": state["graph_state"] + " sad!!"}


def decide_mood(state: SimpleState) -> Literal["node2", "node3"]:
    user_input = state["graph_state"]
    if random.random() > 0.5:
        return "node2"
    return "node3"


# Graph
graph = StateGraph(state_schema=SimpleState)

# Add Nodes
graph.add_node("node1", node1)
graph.add_node("node2", node2)
graph.add_node("node3", node3)

# Add Edges
graph.add_edge(START, "node1")
graph.add_conditional_edges("node1", decide_mood)
graph.add_edge("node2", END)
graph.add_edge("node3", END)

# Compile
app = graph.compile()
