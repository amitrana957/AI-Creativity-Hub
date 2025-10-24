from typing_extensions import TypedDict
import string
from langgraph.graph import StateGraph, END
import random


class ChainState(TypedDict):
    n: int
    letter: str


def add(state: ChainState) -> ChainState:
    """Increment state[n] by one and generate random character to state[letter] and return updated state"""
    random_letter = random.choice(string.ascii_letters)
    return {**state, "n": state["n"] + 1, "letter": random_letter}


def print_out(state: ChainState) -> ChainState:
    """Just for printing current state"""
    print(f"Current n: {state['n']}, Current letter: {state['letter']}")
    return state


def stop(state: ChainState) -> str | None:
    """If n >= 12, stop workflow; otherwise, go back to 'add'."""
    return END if state["n"] >= 12 else "add"


wf = StateGraph(state_schema=ChainState)
wf.add_node("add", add)
wf.add_node("print", print_out)

wf.add_edge("add", "print")
wf.add_conditional_edges("print", stop)

wf.set_entry_point("add")
app = wf.compile(name="First Workflow")
app.invoke({"n": 0, "letter": ""})
