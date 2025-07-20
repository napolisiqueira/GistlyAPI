from flask import Flask, request, jsonify
import whisper
import os
import tempfile

app = Flask(__name__)

# Carrega o modelo Whisper uma vez ao iniciar a aplicação
# Você pode escolher 'tiny', 'base', 'small', 'medium', 'large'
# 'base' é um bom equilíbrio para começar. 'large' é mais preciso, mas exige mais RAM/GPU.
print("Carregando modelo Whisper. Isso pode levar um tempo...")
model = whisper.load_model("base")
print("Modelo Whisper carregado com sucesso.")

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'audio_file' not in request.files:
        return jsonify({"error": "Nenhum arquivo de áudio fornecido"}), 400

    audio_file = request.files['audio_file']
    if audio_file.filename == '':
        return jsonify({"error": "Nenhum arquivo de áudio selecionado"}), 400

    if audio_file:
        # Salva o arquivo temporariamente para o Whisper processar
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            audio_path = tmp_file.name
            audio_file.save(audio_path)

        try:
            print(f"Iniciando transcrição para: {audio_path}")
            # Transcreve o áudio
            result = model.transcribe(audio_path)
            transcription = result["text"]
            print(f"Transcrição concluída: {transcription[:50]}...") # Log dos primeiros 50 caracteres
            return jsonify({"transcription": transcription}), 200
        except Exception as e:
            print(f"Erro durante a transcrição: {e}")
            return jsonify({"error": f"Erro na transcrição: {str(e)}"}), 500
        finally:
            # Garante que o arquivo temporário seja removido
            os.remove(audio_path)
    return jsonify({"error": "Ocorreu um erro inesperado"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "model_loaded": True}), 200

if __name__ == '__main__':
    # Roda a aplicação Flask na porta 5001
    app.run(host='0.0.0.0', port=5001)



import requests
import json

def generate_text_with_ollama(prompt, model_name="llama3"):
    # O nome do serviço no docker-compose é 'ollama'
    # A porta exposta internamente é 11434
    ollama_api_url = "http://ollama:11434/api/generate"

    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False # Para obter a resposta completa de uma vez
    }

    try:
        response = requests.post(ollama_api_url, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("response") # A resposta do modelo está em 'response'
    except requests.exceptions.RequestException as e:
        print(f"Erro ao chamar a API do Ollama: {e}")
        return None

# Exemplo de uso em uma view Django ou função
# def generate_text_view(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         prompt = data.get('prompt')
#         if not prompt:
#             return JsonResponse({"error": "Prompt não fornecido"}, status=400)
#
#         generated_text = generate_text_with_ollama(prompt)
#
#         if generated_text:
#             return JsonResponse({"status": "success", "generated_text": generated_text})
#         else:
#             return JsonResponse({"status": "error", "message": "Falha na geração de texto"}, status=500)
#     return JsonResponse({"status": "error", "message": "Método não permitido"}, status=400)