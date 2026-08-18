# Usamos uma imagem leve (slim) do Python 3.11
FROM python:3.11-slim

# Evita que o Python gere arquivos .pyc e permite logs em tempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instala dependências de sistema (essenciais para as lógicas do Analista.sh)
RUN apt-get update && apt-get install -y --no-install-recommends \
    iputils-ping \
    sqlite3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia apenas o requirements.txt primeiro para aproveitar o cache do Docker
COPY requirements.txt .

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código do backend
COPY . .

# Variável de ambiente para o caminho do banco de dados
ENV DB_PATH=/var/abastece/dados/abastece.db

# Torna o entrypoint executável
RUN chmod +x /app/entrypoint.sh

# Comando de entrada: verifica o banco e inicia a API
CMD ["/app/entrypoint.sh"]