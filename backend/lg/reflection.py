from typing import TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END


load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=GOOGLE_API_KEY,
    model_kwargs={"system_instruction": "You are assistant"},
)


class OverallState(TypedDict):
    question: str
    answer: str
    notes: str


class InputState(TypedDict):
    question: str


class OutputState(TypedDict):
    answer: str


def thinking_node(state: InputState) -> OverallState:
    print("----- Thinking Node -----")
    return {"answer": "bye", "notes": ".... some notes"}


def answer_node(state: OverallState) -> OutputState:
    print("----- Answer-----")
    return {"answer": "By Lance"}


builder = StateGraph(OverallState, input_schema=InputState, output_schema=OutputState)
builder.add_node("thinking_node", thinking_node)
builder.add_node("answer_node", answer_node)

builder.add_edge(START, "thinking_node")
builder.add_edge("thinking_node", "answer_node")
builder.add_edge("answer_node", END)

graph = builder.compile()

# display(Image(graph.get_graph().draw_mermaid_png()))

graph.invoke({"question": "hello hello"})
