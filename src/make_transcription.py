from src.main import model_llm, tokenizer_llm, device, model_whisper
from http import HTTPStatus
import whisper
import torch
import os


# Logical fuction of the sumarrizing and correct the transcription.
def process_text_with_llm(text_input):
    prompt = (
        f"A seguir, uma transcrição de áudio. Por favor, faça o seguinte:\n"
        f"1. Corrija quaisquer erros gramaticais, ortográficos ou de pontuação no texto."
        f"2. Mantenha o sentido original e a integridade das informações.\n"
        f"3. Resuma o texto corrigido em 3 a 5 frases, destacando os pontos mais importantes.\n\n"
        f"Texto da Transcrição:\n{text_input}\n\n"
        f"Resultado (Texto Corrigido e Resumido):"
    )
    messages = [{"role": "user", "content": prompt}]
    encodeds = tokenizer_llm.apply_chat_template(messages, return_tensors="pt")
    model_inputs = encodeds.to(device)

    generated_ids = model_llm.generate(
        model_inputs,
        max_new_tokens=1000,
        do_sample=True,
        temperature=0.7,
        pad_token_id=tokenizer_llm.eos_token_id,
    )

    decoded_output = tokenizer_llm.batch_decode(
        generated_ids[:, model_inputs.shape[1] :], skip_special_tokens=True
    )[0]
    return decoded_output.strip()


def whisper_transcription(audio_file_path):

    if not os.path.exists(audio_file_path):

        ###### AJEITAR ERRO E RETORNAR UM HTTP
        print(f"Erro: O arquivo de áudio '{audio_file_path}' não foi encontrado.")
        print("Por favor, atualize a variável 'audio_file_path' com o caminho correto.")
    else:
        audio = whisper.load_audio(audio_file_path)
        mel = whisper.log_mel_spectrogram(audio).to(model_whisper.device)

        options = whisper.DecodingOptions(language="pt", fp16=torch.cuda.is_available())
        result = model_whisper.decode(mel, options)

        original_transcription = result.text
        llm_processed_output = process_text_with_llm(original_transcription)
        return llm_processed_output


def get_tw(audio_file_path, audio_file_name):
    try:
        transcription = whisper_transcription(audio_file_path)
        return {
            "filename": audio_file_name,
            "transcription": transcription,
        }, HTTPStatus.OK
    except Exception as e:
        return {
            "erro": f"Ocorreu um erro ao processar o vídeo: {str(e)}"
        }, HTTPStatus.INTERNAL_SERVER_ERROR

# --- TESTES COM DADOS LOCAIS --- #
if __name__ == "__main__":
    file_path = input("Digite o local do arquivo: ")

    print(whisper_transcription(file_path))
