FROM python:3.13-slim

WORKDIR /app

# Instalar dependências do sistema para psycopg2
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Instalar uv para gerenciar dependências
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copiar arquivos de dependência primeiro (cache de camadas)
COPY pyproject.toml uv.lock ./

# Instalar dependências
RUN uv sync --frozen --no-dev

# Copiar código da aplicação
COPY . .

CMD ["uv", "run", "main.py"]
