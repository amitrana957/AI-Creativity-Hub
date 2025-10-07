from models import gemini_llm
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableLambda, RunnableParallel
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

# -------------------------
# System Message
# -------------------------
system_msg = SystemMessagePromptTemplate.from_template(
    "You are a professional text analyzer. Your task is to provide clear, concise, "
    "and accurate summaries of the content provided by the user."
)

# -------------------------
# Human Message
# -------------------------
human_msg = HumanMessagePromptTemplate.from_template(
    "Please provide a detailed summary of the following content:\n{content}\n"
    "The summary should be concise, coherent, and capture the main ideas without adding opinions."
)

# -------------------------
# Sentiment Analysis
# -------------------------
sentiment = (
    ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                "You are an AI sentiment analyzer. "
                "Provide ONLY one word as output: Positive, Neutral, or Negative. "
                "Do NOT include any explanation."
            ),
            HumanMessagePromptTemplate.from_template(
                "Analyze the sentiment of this text:\n{x}"
            ),
        ]
    )
    | gemini_llm
    | StrOutputParser()
)

# -------------------------
# Top Words Extraction
# -------------------------
words = (
    ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                "You are an AI that extracts the most relevant keywords from a given text. "
                "Return ONLY an array of the top 3 keywords, e.g., ['word1','word2','word3']. "
                "Do NOT include explanations or extra text."
            ),
            HumanMessagePromptTemplate.from_template(
                "Extract the top 3 keywords from the following content:\n{x}"
            ),
        ]
    )
    | gemini_llm
    | StrOutputParser()
)

# -------------------------
# Main Summary Chain
# -------------------------
prompt = ChatPromptTemplate.from_messages([system_msg, human_msg])
main_chain = prompt | gemini_llm | StrOutputParser()

# -------------------------
# Combined Chain (Final)
# -------------------------
chain = (
    main_chain
    | RunnableLambda(lambda summary: {"summary": summary, "x": summary})
    | RunnableParallel(
        branches={
            "summary": RunnableLambda(lambda x: x["summary"]),
            "sentiments": sentiment,
            "keywords": words,
        }
    )
    | (lambda x: x["branches"])
)

# -------------------------
# Execution
# -------------------------
input_text = (
    "I really enjoy working with AI models like Gemini and LangChain; they are amazing!"
)

result = chain.invoke({"content": input_text})
print(result)
