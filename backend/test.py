from langchain_huggingface import HuggingFaceEndpoint
import os
from dotenv import load_dotenv

load_dotenv()
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

llm = HuggingFaceEndpoint(
    model="tiiuae/falcon-7b-instruct",
    huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
    temperature=0.7,
    max_new_tokens=256,
    provider="hf-inference"
)

print(llm("Explain reinforcement learning in simple terms"))
