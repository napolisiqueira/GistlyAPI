# Usa uma imagem base Python 3.13
FROM python:3.13-slim-bullseye

# Define variáveis de ambiente
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE djangoapp.settings 

# Define o diretório de trabalho dentro do contêiner para a raiz da sua aplicação
WORKDIR /app

# Instale dependências do sistema necessárias para Node.js e npm
# Certifique-se de que o Node.js e npm sejam instalados corretamente.
# Para Debian/Ubuntu (Bullseye), é recomendado usar o NodeSource para versões mais recentes.
# Vou colocar uma forma genérica que geralmente funciona em imagens slim,
# mas se tiver problemas com o Node.js/npm, esta parte pode precisar de mais atenção.
RUN apt-get update && apt-get install -y ffmpeg libsndfile1 \
    curl \
    && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \ 
    apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*


# Copia o arquivo de dependências do backend
COPY backend/requirements.txt /app/backend/

# Instala as dependências do backend
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Copia o restante do código da sua aplicação Django
COPY backend/ /app/backend/

# --- Seção do Frontend ---
# Copia os arquivos de configuração do frontend para instalar dependências
# Estes arquivos (package.json, package-lock.json) estão diretamente sob 'frontend/'
COPY frontend/package.json /app/frontend/
COPY frontend/package-lock.json /app/frontend/

# Instala as dependências do frontend (opcional na build, mas bom para cache)
# Se você já faz 'npm install' no comando do docker-compose, esta linha pode ser removida
# ou mantida para acelerar builds subsequentes onde as dependências não mudam.
RUN cd /app/frontend && npm install --omit=dev 

# Copia o restante do código do frontend, incluindo a pasta 'src'
# A fonte da cópia é 'frontend/' na sua máquina host (contexto de build)
# O destino é '/app/frontend/' dentro do container
COPY frontend/ /app/frontend/

# Comando padrão - será sobrescrito pelo docker-compose para desenvolvimento
CMD ["python", "/app/backend/manage.py", "runserver", "0.0.0.0:8000"]