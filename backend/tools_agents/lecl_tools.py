import os
import glob
import pandas as pd
from typing import List, Dict, Any

from models import gemini_llm
from langchain.tools import Tool
from langgraph.prebuilt import create_react_agent
from lib.utils import pretty_print

# ----------------------------
# Global cache for datasets
# ----------------------------
DATAFRAME_CACHE: Dict[str, pd.DataFrame] = {}


# ----------------------------
# Tool functions
# ----------------------------
def list_csv_files(input: str = "") -> List[str]:
    """List all CSV files in the data/ folder."""
    files = glob.glob(os.path.join("data", "*.csv"))
    return [os.path.basename(f) for f in files]


def preload_datasets(input: str) -> str:
    """
    Load CSV datasets into memory cache.
    Input format: comma or space separated file names
    """
    parts = input.replace(",", " ").split()
    loaded = []
    cached = []
    for path in parts:
        if path not in DATAFRAME_CACHE:
            full_path = os.path.join("data", path)
            try:
                DATAFRAME_CACHE[path] = pd.read_csv(full_path)
                loaded.append(path)
            except Exception as e:
                return f"Error loading {path}: {e}"
        else:
            cached.append(path)
    return f"Loaded: {loaded}\nCached: {cached}"


def get_dataset_summaries(input: str) -> List[Dict[str, Any]]:
    """
    Return basic summaries of datasets.
    Input: comma or space separated file names
    """
    parts = input.replace(",", " ").split()
    summaries = []
    for path in parts:
        if path not in DATAFRAME_CACHE:
            DATAFRAME_CACHE[path] = pd.read_csv(os.path.join("data", path))
        df = DATAFRAME_CACHE[path]
        summary = {
            "file_name": path,
            "columns": list(df.columns),
            "dtypes": dict(df.dtypes.astype(str)),
        }
        summaries.append(summary)
    return summaries


def call_dataframe_method(input: str) -> str:
    """
    Call a simple DataFrame method like head(), describe() etc.
    Input format: "file_name method_name"
    """
    parts = input.split()
    if len(parts) < 2:
        return "Invalid input. Use: <file_name> <method>"
    file_name = parts[0]
    method = parts[1]

    if file_name not in DATAFRAME_CACHE:
        DATAFRAME_CACHE[file_name] = pd.read_csv(os.path.join("data", file_name))
    df = DATAFRAME_CACHE[file_name]
    func = getattr(df, method, None)
    if not callable(func):
        return f"'{method}' is not a valid DataFrame method."
    try:
        return str(func())
    except Exception as e:
        return f"Error calling {method} on {file_name}: {e}"


# ----------------------------
# Wrap tools as LangChain Tools
# ----------------------------
list_tool = Tool(
    name="ListCSVFiles",
    func=list_csv_files,
    description="Lists all CSV files available in the data folder",
)

preload_tool = Tool(
    name="PreloadDatasets",
    func=preload_datasets,
    description="Loads CSV datasets into memory cache. Input is comma or space separated filenames.",
)

summary_tool = Tool(
    name="DatasetSummaries",
    func=get_dataset_summaries,
    description="Returns summaries of datasets including columns and data types. Input is comma or space separated filenames.",
)

call_method_tool = Tool(
    name="CallDataFrameMethod",
    func=call_dataframe_method,
    description="Calls a pandas DataFrame method like head or describe. Input format: 'file_name method_name'",
)

tools = [list_tool, preload_tool, summary_tool, call_method_tool]

# ----------------------------
# Create LangGraph Agent
# ----------------------------
agent = create_react_agent(
    model=gemini_llm,
    tools=tools,
    prompt="You are a DataWizard AI assistant. You can analyze CSV files in the data folder.",
)

# ----------------------------
# Interactive loop
# ----------------------------
if __name__ == "__main__":
    print("📊 Welcome to DataWizard!")
    print("Type 'exit' or 'quit' to leave.\n")
    while True:
        question = input("You: ").strip()
        if question.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break
        res = agent.invoke({"messages": [("human", question)]})
        pretty_print(res)
