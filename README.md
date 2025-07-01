# GistlyAPI

Uma API Flask para transcrição e resumo de vídeos usando Whisper da OpenAI e o modelo Mistral da HuggingFace.

## ⚙️ Funcionalidades

* Upload de arquivos de vídeo/áudio via rota `POST /gystli/upload_video`
* Transcrição automática com modelo Whisper
* Resumo e correção do texto com LLM (Mistral 7B Instruct)
* Retorno em JSON com transcrição e resumo

## 📦 Instalação

Clone o repositório e instale os requisitos:

```bash
git clone https://github.com/napolisiqueira/GistlyAPI.git
cd GistlyAPI
pip install -r requirements.txt
```

> ⚠️ É necessário ter CUDA instalado (para uso com GPU) e modelos grandes podem exigir >12GB de RAM.

## ⚖️ Configuração

O projeto usa um arquivo `config.py` com os seguintes parâmetros:

```python
UPLOAD_FOLDER = "uploads"
MAX_CONTENT_LENGTH = 512 * 1024 * 1024  # 512MB
ALLOWED_EXTENSIONS = {"mp4", "mov", "avi", "mkv", "mp3", "wav"}
```

A pasta de upload será criada automaticamente na inicialização do app.

## 🚀 Como usar

### Rota de upload e processamento

**POST /gystli/upload\_video**

Payload (multipart/form-data):

* `video`: Arquivo de vídeo ou áudio suportado

**Resposta esperada:**

```json
{
  "filename": "meuvideo.mp4",
  "transcription": "Texto transcrito...",
  "summary": "Resumo gerado..."
}
```

## 🛠️ Estrutura do Projeto

```
GistlyAPI/
├── app.py                 # Inicializa o app Flask
├── config.py              # Configurações globais
├── routes.py              # Rotas HTTP
├── services.py            # Lógica de transcrição e resumo
├── llm_loader.py          # Carregamento dos modelos Whisper e Mistral
├── utils.py               # Funções auxiliares
├── uploads/               # Pasta de upload criada dinamicamente
├── requirements.txt       # Dependências do projeto
```

## 📌 Tecnologias e Modelos

* **Flask**: framework web Python
* **OpenAI Whisper (base)**: transcrição de áudio
* **Mistral 7B Instruct**: gera resumos com correção gramatical
* **Transformers** (HuggingFace): interface com modelos LLM

## ✅ Exemplos com cURL

```bash
curl -X POST http://localhost:5000/gystli/upload_video \
  -F video=@caminho/para/video.mp4
```

## 🚧 Boas práticas

* Limite de 512MB por upload
* Apenas formatos permitidos (mp4, mov, avi, mkv, mp3, wav)
* Lide com erros como:

  * Tipo de arquivo não permitido
  * Arquivo corrompido
  * Erros do modelo

## 📄 Licença

Distribuído sob a licença MIT.

## 🧠 Ideias futuras

* Interface web para uploads
* Geração de legendas
* Tradução automática
* Integração com links do YouTube ou Google Drive
