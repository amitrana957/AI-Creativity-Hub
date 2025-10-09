from langchain_core.runnables import RunnableBranch, RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from lib import DebugRunnable
from models import gemini_llm


def DebugCondition(name, condition_fn, color="\033[1;33m"):  # yellow
    """Wraps a branch condition to print evaluation result."""
    reset = "\033[0m"
    return lambda x: (
        print(f"{color}[DEBUG] {name} CONDITION:{reset} {condition_fn(x)}")
        or condition_fn(x)
    )


# -----------------------------
# Branch conditions
# -----------------------------
is_positive = DebugCondition("Positive Branch", lambda x: "good" in x.lower())
is_negative = DebugCondition("Negative Branch", lambda x: "bad" in x.lower())

# -----------------------------
# Runnable branches with debug
# -----------------------------
branches = RunnableBranch(
    (
        is_positive,
        DebugRunnable("Positive Runnable Before LLM")
        | ChatPromptTemplate.from_template(template="Positive feedback: {input}")
        | gemini_llm
        | StrOutputParser()
        | DebugRunnable("Positive Runnable After Parser", color="\033[1;32m"),  # green
    ),
    (
        is_negative,
        DebugRunnable("Negative Runnable Before LLM")
        | ChatPromptTemplate.from_template(template="Negative feedback: {input}")
        | gemini_llm
        | StrOutputParser()
        | DebugRunnable("Negative Runnable After Parser", color="\033[1;31m"),  # red
    ),
    # Default branch
    DebugRunnable("Default Runnable Before LLM")
    | ChatPromptTemplate.from_template(template="Neutral feedback: {input}")
    | gemini_llm
    | StrOutputParser()
    | DebugRunnable("Default Runnable After Parser", color="\033[1;36m"),  # cyan
)

# -----------------------------
# Test input
# -----------------------------
feedback = "The product quality is good"
result = branches.invoke(feedback)
print("\033[1;35m[FINAL RESULT]\033[0m", result)
