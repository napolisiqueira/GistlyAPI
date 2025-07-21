<body>
    <div class="container">
        <h1>GistlyAPI</h1>
        <p>Uma API Flask para transcrição e resumo de vídeos usando Whisper da OpenAI e o modelo Mistral da HuggingFace.</p>

  <h2>⚙️ Funcionalidades</h2>
  <ul>
      <li>Upload de arquivos de vídeo/áudio via rota <code>POST /gystli/upload_video</code></li>
      <li>Transcrição automática com modelo Whisper</li>
      <li>Resumo e correção do texto com LLM (Mistral 7B Instruct)</li>
      <li>Retorno em JSON com transcrição e resumo</li>
  </ul>

  <h2>📦 Instalação</h2>
  <p>Clone o repositório e instale os requisitos:</p>
  <pre><code>git clone https://github.com/napolisiqueira/GistlyAPI.git
cd GistlyAPI
pip install -r requirements.txt</code></pre>
        <p><strong>⚠️ É necessário ter CUDA instalado (para uso com GPU) e modelos grandes podem exigir &gt;12GB de RAM.</strong></p>

  <h2>⚖️ Configuração</h2>
  <p>O projeto usa um arquivo <code>config.py</code> com os seguintes parâmetros:</p>
  <pre><code>UPLOAD_FOLDER = "uploads"
MAX_CONTENT_LENGTH = 512 * 1024 * 1024  # 512MB
ALLOWED_EXTENSIONS = {"mp4", "mov", "avi", "mkv", "mp3", "wav"}
</code></pre>
        <p>A pasta de upload será criada automaticamente na inicialização do app.</p>

  <h2>🚀 Como usar</h2>
  <h3>Rota de upload e processamento</h3>
  <p><strong>POST /gystli/upload_video</strong></p>
  <p>Payload (multipart/form-data):</p>
  <ul>
      <li><code>video</code>: Arquivo de vídeo ou áudio suportado</li>
  </ul>
  <p><strong>Resposta esperada:</strong></p>
  <pre><code>{
  "filename": "meuvideo.mp4",
  "transcription": "Texto transcrito...",
  "summary": "Resumo gerado..."
}</code></pre>

  <h2>🛠️ Estrutura do Projeto</h2>
  <pre><code>GistlyAPI/
├── app.py                 # Inicializa o app Flask
├── config.py              # Configurações globais
├── routes.py              # Rotas HTTP
├── services.py            # Lógica de transcrição e resumo
├── llm_loader.py          # Carregamento dos modelos Whisper e Mistral
├── utils.py               # Funções auxiliares
├── uploads/               # Pasta de upload criada dinamicamente
├── requirements.txt       # Dependências do projeto
</code></pre>

  <h2>📌 Tecnologias e Modelos</h2>
  <ul>
      <li><strong>Flask</strong>: framework web Python</li>
      <li><strong>OpenAI Whisper (base)</strong>: transcrição de áudio</li>
      <li><strong>Mistral 7B Instruct</strong>: gera resumos com correção gramatical</li>
      <li><strong>Transformers</strong> (HuggingFace): interface com modelos LLM</li>
  </ul>

  <h2>✅ Exemplos com cURL</h2>
  <pre><code>curl -X POST http://localhost:5000/gystli/upload_video \
  -F video=@caminho/para/video.mp4
</code></pre>

  <h2>🚧 Boas práticas</h2>
  <ul>
      <li>Limite de 512MB por upload</li>
      <li>Apenas formatos permitidos (mp4, mov, avi, mkv, mp3, wav)</li>
      <li>Lide com erros como:
          <ul>
              <li>Tipo de arquivo não permitido</li>
              <li>Arquivo corrompido</li>
              <li>Erros do modelo</li>
          </ul>
      </li>
  </ul>

  <h2>📄 Licença</h2>
  <p>Distribuído sob a licença MIT.</p>

  <h2>🧠 Ideias futuras</h2>
  <ul>
      <li>Interface web para uploads</li>
      <li>Geração de legendas</li>
      <li>Tradução automática</li>
      <li>Integração com links do YouTube ou Google Drive</li>
  </ul>
</div>
</body>
</html>
