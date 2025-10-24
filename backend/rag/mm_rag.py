from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from PIL import Image
import base64
import requests
from io import BytesIO
import os
from pathlib import Path

# Load environment
from dotenv import load_dotenv

from lib.utils import pretty_print

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# --- 1. Initialize models ---
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=GOOGLE_API_KEY)

# Use CLIP or ViT model for image embeddings
image_embeddings = HuggingFaceEmbeddings(model_name="openai/clip-vit-base-patch32")

# --- 2. Load an image ---
image_url = (
    "https://4.img-dpreview.com/files/p/E~TS590x0~articles/3925134721/0266554465.jpeg"
)
response = requests.get(image_url)
image = Image.open(BytesIO(response.content))

# Convert image to base64 (for LLM input if needed)
buffer = BytesIO()
image.save(buffer, format="PNG")
img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

# --- 3. Create image embeddings ---
image_vector = image_embeddings.embed_query(img_base64)

# --- 4. Store in Chroma DB ---
DB_DIR = Path(__file__).parent / "db" / "mm_rag_db"
os.makedirs(DB_DIR, exist_ok=True)

vector_db = Chroma(
    collection_name="images",
    embedding_function=image_embeddings,
    persist_directory=DB_DIR,
)

# You can store the embedding with metadata (e.g., image name, tags)
vector_db.add_texts(
    texts=["Apple image"],  # text label
    embeddings=[image_vector],
    metadatas=[{"source": "apple.jpg", "type": "image"}],
)

# --- 5. Query ---
question = "What fruit is shown in the image?"
query_vector = image_embeddings.embed_query(img_base64)

similar = vector_db.similarity_search_by_vector(query_vector, k=1)
context = similar[0].metadata["source"]

# --- 6. Generate response with Gemini ---
prompt = ChatPromptTemplate.from_template(
    """
You are a multimodal assistant.
Given the image and its description, answer the question.
Context: {context}
Question: {question}
Answer:
"""
)

formatted = prompt.format(context=context, question=question)
result = llm.invoke(formatted)

pretty_print("🔹 Response:", result.content.strip())
