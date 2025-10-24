from models import gemini_llm
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from lib.utils import pretty_print
from langchain.schema import HumanMessage
from typing_extensions import TypedDict


class TipCalculationState(TypedDict):
    total_bill: float
    tip_percent: float
    tip_amount: float
    total_with_tip: float


@tool
def calculate_tip(state: TipCalculationState) -> TipCalculationState:
    """Calculate tip amount"""
    tip = state["total_bill"] * state["tip_percent"] / 100
    state["tip_amount"] = tip
    return state


@tool
def calculate_total_with_tip(state: TipCalculationState) -> TipCalculationState:
    """Calculate total bill including tip"""
    state["total_with_tip"] = state["total_bill"] + state["tip_amount"]
    return state


tools = [calculate_total_with_tip, calculate_tip]
tip_agent = create_react_agent(
    model=gemini_llm,
    tools=[calculate_tip, calculate_total_with_tip],
    prompt=(
        "You are a restaurant assistant. "
        "When a user provides a query like 'I have a bill of $125 and want to tip 16%', "
        "extract total_bill and tip_percent from it and use the tools to calculate results."
    ),
)

question = (
    "I have a bill of $125 and want to tip 16%. Tell me the tip and total amount."
)

state: TipCalculationState = {
    "total_bill": 0.0,
    "tip_percent": 0.0,
    "tip_amount": 0.0,
    "total_with_tip": 0.0,
}


response = tip_agent.invoke({"messages": [HumanMessage(question)], "state": state})

pretty_print(response)
pretty_print(f"Question: {question}\nAnswer: " + response["messages"][-1].content)
