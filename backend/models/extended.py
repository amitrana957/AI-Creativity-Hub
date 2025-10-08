from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEndpointEmbeddings

# ---------------- Load environment variables ----------------
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# ---------------- Initialize the Gemini LLM ----------------
gemini_llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=GOOGLE_API_KEY)

# ---------------- Initialize the Hugging Face Embeddings ----------------
hf_embeddings = HuggingFaceEndpointEmbeddings(
    model="sentence-transformers/all-MiniLM-L6-v2",  # Model name as a keyword argument
    task="feature-extraction",
    huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
)


if __name__ == "__main__":
    # # Test embeddings
    # vector = hf_embeddings.embed_query("Hello world")
    # print("Embedding vector (first 10 values):", vector[:10])

    # # Test LLM
    # response = gemini_llm.invoke("Write a short greeting.")
    # print("Gemini LLM response:", response.content)
    pass
