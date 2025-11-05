from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain.tools import tool
from langgraph.graph import StateGraph, MessagesState
from langgraph.prebuilt import ToolNode

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")


@tool
def get_weather(location: str):
    """Get weather from API and return"""
    return f"Current weather in {location}: 23 degree celsius"


def llm_calling(state: MessagesState) -> MessagesState:
    return {"messages": llm.invoke(state["messages"])}


builder = StateGraph(MessagesState)
builder.add_node("llm_calling", llm_calling)
builder.add_node("tools", ToolNode([get_weather]))

