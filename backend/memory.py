from models import gemini_llm
from langchain.memory import ConversationSummaryBufferMemory

# ---------------- Memory store ----------------
# Each session_id gets its own ConversationBufferMemory
session_memories: dict[str, ConversationSummaryBufferMemory] = {}


# ---------------- Ask function ----------------
def ask_text_model(user_input: str, session_id: str = "default") -> str:
    """
    Generate a response from Gemini using ConversationBufferMemory per session.

    Args:
        user_input (str): User prompt.
        session_id (str): Identifier for session memory.

    Returns:
        str: Model response.
    """
    # Initialize memory for new sessions
    if session_id not in session_memories:
        session_memories[session_id] = ConversationSummaryBufferMemory(
            memory_key="chat_history", return_messages=True
        )

    memory = session_memories[session_id]

    # Get current chat history
    history = memory.load_memory_variables({})["chat_history"]

    # Prepare input for Gemini: include previous messages + new user input
    # Convert LangChain messages to Gemini's expected dict format
    input_history = [
        (
            {"type": "human", "content": msg.content}
            if msg.type == "human"
            else {"type": "ai", "content": msg.content}
        )
        for msg in history
    ]
    input_history.append({"type": "human", "content": user_input})

    # Call Gemini
    response = gemini_llm.invoke(input_history)
    ai_text = response.content.strip()

    # Update memory with new messages
    memory.chat_memory.add_user_message(user_input)
    memory.chat_memory.add_ai_message(ai_text)

    return ai_text
