from models import gemini_llm
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableLambda, RunnableSequence

messages = [
    ("system", "You are standup comedian"),
    ("human", "tell me a {count} jokes about {category}"),
]
prompt = ChatPromptTemplate(messages=messages)

chain = prompt | gemini_llm | StrOutputParser()
result = chain.invoke({"count": 1, "category": "AI"})
print(result)


first = RunnableLambda(lambda x: prompt.format_prompt(**x))
middle = RunnableLambda(lambda x: gemini_llm.invoke(x.to_messages()))
last = RunnableLambda(lambda x: x.content)

chain1 = RunnableSequence(first=first, middle=[middle], last=last)
print(chain1.invoke({"count": 1, "category": "AI"}))
