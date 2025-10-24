from langgraph.prebuilt import create_react_agent
from langchain.tools import tool
from models import gemini_llm
from lib.utils import pretty_print

# ---------- TOOLS ----------


@tool
def get_temperature(city: str) -> dict:
    """
    Returns the current temperature (Celsius) of a given city.
    """
    temp_data = {"New York": 22, "London": 16, "Mumbai": 30, "Kangra": 20}
    temp = temp_data.get(city)
    if temp is None:
        return {"error": f"No data available for {city}"}
    return {"city": city, "temperature_c": temp}


@tool
def convert_temp(celsius: float, to_scale: str = "F") -> float:
    """
    Converts temperature from Celsius to Fahrenheit or vice versa.
    """
    if to_scale.upper() == "F":
        return celsius * 9 / 5 + 32
    elif to_scale.upper() == "C":
        return (celsius - 32) * 5 / 9
    else:
        return "Invalid scale. Use 'C' or 'F'."


@tool
def hot_or_cold(celsius: float) -> str:
    """
    Returns a description if the temperature is hot, cold, or moderate.
    """
    if celsius >= 30:
        return "It's hot!"
    elif celsius <= 15:
        return "It's cold!"
    else:
        return "The temperature is moderate."


# ---------- HYBRID TOOL CALLING AGENT ----------


class HybridToolCallingAgent:
    def __init__(self, llm, tools, auto_tool_call=True):
        self.agent = create_react_agent(
            model=llm,
            tools=tools,
            prompt="You are a Weather Assistant. You can get temperature, convert it, and describe if it is hot or cold.",
        )
        self.tools_map = {t.name: t for t in tools}
        self.auto_tool_call = auto_tool_call

    def run(self, query: str) -> str:
        # Step 1: LLM generates response
        response = self.agent.invoke({"messages": [("human", query)]})

        if self.auto_tool_call:
            # Automatic: LangGraph handles tool calls internally
            return response

        # Manual tool invocation: intercept and execute tool calls
        tool_calls = response.get("tool_calls") or []
        chat_history = [("human", query)]

        for call in tool_calls:
            tool_name = call["name"]
            tool_args = call["args"]
            tool_result = self.tools_map[tool_name].invoke(**tool_args)
            # Feed tool result back to agent
            chat_history.append(("tool", f"{tool_name} output: {tool_result}"))

        # Final LLM response after manual tool handling
        final_response = self.agent.invoke({"messages": chat_history})
        return final_response

    def extract_full_conversation(self, response):
        full_text = []
        messages = response.get("messages") or []
        for msg in messages:
            msg_type = type(msg).__name__
            content = getattr(msg, "content", None)
            if content:
                full_text.append(f"[{msg_type}] {content}")
        return "\n".join(full_text)


# ---------- USAGE ----------

tools = [get_temperature, convert_temp, hot_or_cold]
weather_agent = HybridToolCallingAgent(gemini_llm, tools, auto_tool_call=False)

question = "What is the temperature in Kangra and is it hot or cold? Convert it to Fahrenheit as well."

response = weather_agent.run(question)
pretty_print(response)
pretty_print(weather_agent.extract_full_conversation(response))
