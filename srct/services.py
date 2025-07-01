from models_loader import model_llm, tokenizer_llm, device, model_whisper
from http import HTTPStatus
import torch
import whisper
import os

def process_text_with_llm(text_input):
    prompt = (
        f"A seguir, uma transcrição de áudio. Por favor, faça o seguinte:\n"
        f"1. Corrija erros gramaticais e ortográficos.\n"
        f"2. Mantenha o sentido original.\n"
        f"3. Resuma em 3 a 5 frases os principais pontos.\n\n"
        f"Transcrição:\n{text_input}\n\n"
        f"Resultado:"
    )

    messages = [{"role": "user", "content": prompt}]
    encoded = tokenizer_llm.apply_chat_template(messages, return_tensors="pt").to(device)

    output_ids = model_llm.generate(
        encoded,
        max_new_tokens=1000,
        do_sample=True,
        temperature=0.7,
        pad_token_id=tokenizer_llm.eos_token_id,
    )

    return tokenizer_llm.batch_decode(output_ids[:, encoded.shape[1]:], skip_special_tokens=True)[0].strip()

def whisper_transcription(audio_file_path):
    if not os.path.exists(audio_file_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {audio_file_path}")

    audio = whisper.load_audio(audio_file_path)
    mel = whisper.log_mel_spectrogram(audio).to(model_whisper.device)

    options = whisper.DecodingOptions(language="pt", fp16=torch.cuda.is_available())
    result = model_whisper.decode(mel, options)

    return result.text

def transcribe_and_summarize(audio_path, filename):
    try:
        transcription = whisper_transcription(audio_path)
        summary = process_text_with_llm(transcription)

        return {
            "filename": filename,
            "transcription": transcription,
            "summary": summary
        }, HTTPStatus.OK

    except Exception as e:
        return {"erro": str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR
