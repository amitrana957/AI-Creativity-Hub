from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain_huggingface import HuggingFacePipeline


# ---------------- Model setup ----------------
tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = AutoModelForCausalLM.from_pretrained("gpt2")

hf_pipeline = pipeline(
    task="text-generation",
    model="gemini-2.5-flash",
    tokenizer=tokenizer,
    max_new_tokens=10,  # length of response
    temperature=0.7,  # creativity
    pad_token_id=tokenizer.eos_token_id,
)

llm = HuggingFacePipeline(pipeline=hf_pipeline)


def ask_text_model(user_input: str, session_id: str) -> str:
    try:
        # Generate response
        response = llm.invoke(user_input)
        return response.content.strip()
    except Exception as e:
        return f"Error generating response: {str(e)}"
