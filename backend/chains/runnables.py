from langchain.prompts import ChatPromptTemplate
from lib import DebugRunnable
from models import gemini_llm
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import (
    RunnableMap,
    RunnableLambda,
)


# Define individual Runnables
sentiment_analysis_runnable = RunnableLambda(
    lambda text: "Positive" if "good" in text["input"].lower() else "Negative"
)

summarization_runnable = (
    ChatPromptTemplate.from_template(template="Summarize this: {input}")
    | gemini_llm
    | StrOutputParser()
)

# Combine Runnables into a pipeline
pipeline = RunnableMap(
    {"sentiment": sentiment_analysis_runnable, "summary": summarization_runnable}
)


# Invoke the pipeline
feedback = "The product quality is really bad and exceeded expectations."
result = pipeline.invoke({"input": feedback})

print(result)
