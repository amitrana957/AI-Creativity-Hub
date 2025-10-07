# models/gemini_model.py
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

# ---------------- Load environment variables ----------------
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# ---------------- Initialize the Gemini model ----------------
gemini_llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=GOOGLE_API_KEY)
