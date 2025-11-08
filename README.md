<h1 align="center">🦾 GistlyAPI: Experimentos com IA - Flask + Whisper + Mistral</h1>
<p align="center">
    <b>API Flask experimental para transcrição de vídeo/áudio e geração de resumo via IA. Nunca foi terminada, e atualmente não há intenções disso.<br>
    Feita apenas para <strong>testes e estudo local</strong>, agregando modelos Whisper (OpenAI) e Mistral (HuggingFace).
    </b>
</p>

<hr/>

<h2>⚙️ Funcionalidades</h2>
<ul>
    <li>Upload de arquivos de vídeo/áudio (<code>POST /gystli/upload_video</code>)</li>
    <li>Transcrição automática com <b>Whisper</b></li>
    <li>Resumo e correção do texto usando <b>Mistral 7B Instruct</b></li>
    <li>Resposta em JSON com transcrição e resumo</li>
</ul>

<p style="color:red"><b>IMPORTANTE:</b> Projeto não finalizado, nem recomendado para produção. Voltado para experimentação local com IA e integração entre APIs.</p>

<hr/>

<h2>📦 Instalação</h2>
<ol>
    <li>Clone o repositório:
        <pre><code>git clone https://github.com/napolisiqueira/GistlyAPI.git
cd GistlyAPI
pip install -r requirements.txt
        </code></pre>
    </li>
    <li><b>Necessário:</b> CUDA instalado para uso de GPU <br>
        Modelos grandes podem exigir &gt;12GB de RAM</li>
</ol>

<hr/>

<h2>⚖️ Configuração</h2>
<p>Defina parâmetros em <code>config.py</code>:</p>
<pre><code>UPLOAD_FOLDER = "uploads"
MAX_CONTENT_LENGTH = 512 * 1024 * 1024  # 512MB
ALLOWED_EXTENSIONS = {"mp4", "mov", "avi", "mkv", "mp3", "wav"}
</code></pre>
<p>A pasta de upload é criada ao inicializar o app.</p>

<hr/>

<h2>🚀 Como usar</h2>
<p><b>Endpoint de processamento:</b></p>
<code>POST /gystli/upload_video</code>
<p><b>Payload:</b> multipart/form-data (<code>video</code>: arquivo de vídeo/áudio)</p>
<p><b>Resposta:</b></p>
<pre><code>{
  "filename": "meuvideo.mp4",
  "transcription": "Texto transcrito...",
  "summary": "Resumo gerado..."
}
</code></pre>
<p><b>Exemplo com cURL:</b></p>
<pre><code>curl -X POST http://localhost:5000/gystli/upload_video \
  -F video=@caminho/para/video.mp4
</code></pre>

<hr/>

<h2>🛠️ Estrutura do Projeto</h2>
<pre><code>GistlyAPI/
├── app.py           # Inicializa o Flask
├── config.py        # Configurações
├── routes.py        # Rotas HTTP
├── services.py      # Transcrição e resumo
├── llm_loader.py    # Carregamento dos modelos
├── utils.py         # Funções extras
├── uploads/         # Pasta dinâmica para arquivos
├── requirements.txt # Dependências
</code></pre>

<hr/>

<h2>📌 Tecnologias e Modelos Utilizados</h2>
<ul>
    <li>Flask (web API Python)</li>
    <li>OpenAI Whisper (transcrição de áudio)</li>
    <li>Mistral 7B Instruct (resumo de texto)</li>
    <li>Transformers/HuggingFace</li>
</ul>

<hr/>

<h2>🚧 Boas Práticas & Limitações</h2>
<ul>
    <li>Limite: 512MB por upload</li>
    <li>Formatos aceitos: mp4, mov, avi, mkv, mp3, wav</li>
    <li>Tratamento de erros:
        <ul>
            <li>Arquivo inválido</li>
            <li>Arquivo corrompido</li>
            <li>Falha de modelo/infra</li>
        </ul>
    </li>
</ul>

<hr/>

<h2>👨‍💻 Autor</h2>
<ul>
    <li>Felipe Napoli Siqueira</li>
    <li><a href="https://github.com/napolisiqueira">@napolisiqueira</a></li>
</ul>
