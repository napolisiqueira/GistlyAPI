from transformers import AutoModelForCausalLM, AutoTokenizer
from flask import Flask
from routes import app as gystly_blueprint
import whisper
import torch
import os

app = Flask()
# Configurações
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["MAX_CONTENT_LENGTH"] = 512 * 1024 * 1024  # Limite: 512MB
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
app.register_blueprint(gystly_blueprint)

# Initial conf
model_whisper = whisper.load_model("base")
MODEL_NAME_LLM = "mistralai/Mistral-7B-Instruct-v0.2"
device = "cuda" if torch.cuda.is_available() else "cpu"
# Laod the LLM with the confs and conf the tokens (float16 for better devices and float32 for old devices)
tokenizer_llm = AutoTokenizer.from_pretrained(MODEL_NAME_LLM)
model_llm = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME_LLM,
    torch_dtype=torch.bfloat16 if device == "cuda" else torch.float32,
    device_map="auto" if device == "cuda" else None,
)
if device == "cpu":
    model_llm.to(device)
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {"mp4", "mov", "avi", "mkv", "ffmpeg", "mp3", "wav"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS




if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
