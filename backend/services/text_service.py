import time
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

model_name = "google/flan-t5-small"
# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)


def ask_text_model(query: str):
    """
    Generate an answer to a question using a closed-book QA model.
    - query: the question string
    """
    time.sleep(2)

    # Prepare the input
    input_text = f"Question: {query} Answer:"
    inputs = tokenizer(input_text, return_tensors="pt")

    # Generate the answer
    with torch.no_grad():
        outputs = model.generate(inputs["input_ids"], max_length=50)

    # Decode the generated answer
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer.strip() or "Sorry, I could not find an answer."
