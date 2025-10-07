"""
This file contains a collection of prompt templates using LangChain.
Designed for quick reference and reuse in backend pipelines.
Includes:
- Basic: Simple system/human prompts
- Zero-shot, Few-shot
- Advanced: Chain-of-Thought, Structured/JSON, Dynamic/Multi-turn, Self-Aware/Tree-of-Thought
- Demo: Format vs Invoke behavior
- Quick hints for interview memory recall
"""

from langchain.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.prompts.few_shot import FewShotPromptTemplate
from models.gemini_model import gemini_llm

# -------------------------------
# BASIC PROMPT TEMPLATES
# -------------------------------
# Hint: Simple single-turn chat, good for quick questions
basic_system_msg = SystemMessagePromptTemplate.from_template(
    "You are a helpful AI assistant."
)
basic_human_msg = HumanMessagePromptTemplate.from_template("{user_input}")
basic_prompt = ChatPromptTemplate.from_messages([basic_system_msg, basic_human_msg])
# Example usage:
# basic_prompt.format_messages(user_input="What is Python?")

# -------------------------------
# 1️⃣ ZERO-SHOT PROMPTING
# -------------------------------
# Hint: No examples needed, instructions only
zero_shot_template = PromptTemplate(
    input_variables=["question"],
    template="""
Answer the following question clearly and concisely:

Question: {question}
Answer:
""",
)
# Example:
# zero_shot_template.format(question="What is the capital of France?")

# -------------------------------
# 2️⃣ FEW-SHOT PROMPTING (official LangChain class)
# -------------------------------
# Hint: Provide examples to guide response
example_prompt = PromptTemplate.from_template("Q: {question}\nA: {answer}")

examples = [
    {
        "question": "What is the largest planet in our solar system?",
        "answer": "Jupiter",
    },
    {"question": "Who wrote '1984'?", "answer": "George Orwell"},
]

few_shot_template = FewShotPromptTemplate(
    example_prompt=example_prompt,
    examples=examples,
    input_variables=["question"],
    prefix="Answer the questions based on the examples below:\n",
    suffix="\n{question}\nA:",
)
# Example:
# few_shot_template.format(question="What is the capital of Japan?")

# -------------------------------
# 3️⃣ CHAIN-OF-THOUGHT (CoT)
# -------------------------------
# Hint: Step-by-step reasoning, useful for math/logical problems
cot_template = PromptTemplate(
    input_variables=["problem"],
    template="""
Solve the following problem step by step. Show your reasoning first, then give the final answer.

Problem: {problem}
""",
)
# Example:
# cot_template.format(problem="If a train travels 60 miles in 1.5 hours, what is its speed?")

# -------------------------------
# 4️⃣ STRUCTURED / JSON OUTPUT
# -------------------------------
# Hint: Force AI to respond in machine-readable format
structured_system_msg = SystemMessagePromptTemplate.from_template(
    "You are a JSON generator. Respond ONLY in this format: {{'name': '', 'age': 0, 'city': ''}}"
)
structured_human_msg = HumanMessagePromptTemplate.from_template(
    "Extract the information from the text: {text}"
)
structured_prompt = ChatPromptTemplate.from_messages(
    [structured_system_msg, structured_human_msg]
)
# Example:
# structured_prompt.format_messages(text="Alice is 30 years old and lives in London.")

# -------------------------------
# 5️⃣ DYNAMIC / MULTI-TURN
# -------------------------------
# Hint: Multi-turn conversations, dynamic placeholders
multi_turn_messages = [
    ("system", "You are a helpful assistant. Remember context: {context}"),
    ("human", "{user_input}"),
]
multi_turn_prompt = ChatPromptTemplate.from_messages(multi_turn_messages)
# Example:
# multi_turn_prompt.format_messages(context="Python question", user_input="Explain decorators.")

# -------------------------------
# 6️⃣ SELF-AWARE / TREE-OF-THOUGHT (ToT)
# -------------------------------
# Hint: Generate multiple reasoning paths, self-evaluate, reduce hallucinations
self_aware_system_msg = SystemMessagePromptTemplate.from_template(
    "You are a careful AI. Generate 3 alternative reasoning paths first, "
    "then evaluate them, and finally give the most logical answer."
)
self_aware_human_msg = HumanMessagePromptTemplate.from_template("{question}")
self_aware_prompt = ChatPromptTemplate.from_messages(
    [self_aware_system_msg, self_aware_human_msg]
)
# Example:
# self_aware_prompt.format_messages(question="If a train travels 60 miles in 1.5 hours, what is its speed?")

# -------------------------------
# ⚡ FORMAT vs INVOKE DEMO
# -------------------------------
# Hint: Understand when placeholders are filled vs when LLM is called
system_msg_demo = SystemMessagePromptTemplate.from_template(
    "You are a helpful assistant."
)
human_msg_demo = HumanMessagePromptTemplate.from_template(
    "Explain {topic} in simple terms."
)
chat_prompt_demo = ChatPromptTemplate.from_messages([system_msg_demo, human_msg_demo])

# Format messages only
formatted_messages = chat_prompt_demo.format_messages(topic="OpenAI")
print("\n--- FORMAT_MESSAGES ---")
print(formatted_messages)

# Invoke on template without LLM → just formats messages
invoke_without_llm = chat_prompt_demo.invoke({"topic": "OpenAI"})
print("\n--- INVOKE WITHOUT LLM ---")
print(invoke_without_llm)

# Invoke with LLM → produces AI response
ai_response = gemini_llm.invoke(formatted_messages)
print("\n--- INVOKE WITH LLM ---")
print(ai_response.content)

# -------------------------------
# EXAMPLES / QUICK REFERENCE
# -------------------------------
if __name__ == "__main__":
    # Basic Example
    print("\n----- BASIC PROMPT -----")
    print(basic_prompt.format_messages(user_input="What is Python?"))

    # Zero-Shot Example
    print("\n----- ZERO-SHOT -----")
    print(zero_shot_template.format(question="What is the capital of France?"))

    # Few-Shot Example
    print("\n----- FEW-SHOT -----")
    print(few_shot_template.format(question="What is the capital of Japan?"))

    # CoT Example
    print("\n----- CHAIN-OF-THOUGHT -----")
    print(
        cot_template.format(
            problem="If a train travels 60 miles in 1.5 hours, what is its speed?"
        )
    )

    # Structured / JSON Example
    print("\n----- STRUCTURED / JSON -----")
    text = "Alice is 30 years old and lives in London."
    print(structured_prompt.format_messages(text=text))

    # Multi-Turn Example
    print("\n----- MULTI-TURN -----")
    print(
        multi_turn_prompt.format_messages(
            context="User asked about Python programming.",
            user_input="Explain what a decorator is.",
        )
    )

    # Self-Aware / Tree-of-Thought Example
    print("\n----- SELF-AWARE / TREE-OF-THOUGHT -----")
    question = "If a train travels 60 miles in 1.5 hours, what is its speed?"
    print(self_aware_prompt.format_messages(question=question))
