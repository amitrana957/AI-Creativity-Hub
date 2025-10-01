from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
from typing import Dict, List

# ---------------- Load .env variables ----------------
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# ---------------- Initialize the Gemini model ----------------
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=GOOGLE_API_KEY)

# ---------------- Session history store ----------------
# Each session_id has its own conversation history
conversation_histories: Dict[str, List[Dict[str, str]]] = {}


# ---------------- Ask function ----------------
def ask_text_model(user_input: str, session_id: str = "default") -> str:
    """
    Generate a response from Gemini with conversation history per session.

    Args:
        user_input (str): User prompt.
        session_id (str): Identifier for session history.

    Returns:
        str: Model response.
    """
    # Initialize history for new sessions
    if session_id not in conversation_histories:
        conversation_histories[session_id] = []

    history = conversation_histories[session_id]

    # Add user input to history
    history.append({"type": "human", "content": user_input})

    # Call Gemini with full session history
    response = llm.invoke(history)
    ai_text = response.content.strip()

    # Add AI response to history
    history.append({"type": "ai", "content": ai_text})

    return ai_text
