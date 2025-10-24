from langchain.tools import Tool, tool
from langchain.agents import initialize_agent
from models import gemini_llm
from langgraph.prebuilt import create_react_agent

from lib.utils import pretty_print


@tool
def add_numbers(input: str) -> dict:
    """
    Adds all numeric values found in a string and returns the sum in a dictionary.
    """
    numbers = [int(x) for x in input.replace(",", " ").split() if x.isdigit()]
    return {"result": sum(numbers)}


# agent = initialize_agent(
#     tools=[add_numbers],
#     llm=gemini_llm,
#     verbose=True,
#     handle_parsing_errors=True,
# )


question = "Kangra has total 542 persons, In bilaspur there are 463 and in Mandi there are 1000, what will be the total? Also tell me about waht and which I'm talking about"

# response = agent.invoke(question)

## LangGraph
add_agent = create_react_agent(
    model=gemini_llm, tools=[add_numbers], prompt="YOu are AI assitant"
)

add_res = add_agent.invoke({"messages": [("human", question)]})
pretty_print(add_res)
