import whisper
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Whisper
model_whisper = whisper.load_model("base")

# LLM
MODEL_NAME_LLM = "mistralai/Mistral-7B-Instruct-v0.2"
device = "cuda" if torch.cuda.is_available() else "cpu"

tokenizer_llm = AutoTokenizer.from_pretrained(MODEL_NAME_LLM)

model_llm = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME_LLM,
    torch_dtype=torch.bfloat16 if device == "cuda" else torch.float32,
    device_map="auto" if device == "cuda" else None,
)

if device == "cpu":
    model_llm.to(device)
