#!/bin/bash

# Verifica se o banco de dados já existe
if [ ! -f "$DB_PATH" ]; then
  echo "Banco não encontrado em $DB_PATH. Executando simulador..."
  python /scripts/simulador_posto.py
fi

# Inicia a API
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
