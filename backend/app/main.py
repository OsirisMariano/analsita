from fastapi import FastAPI, HTTPException
import sqlite3
import os

app = FastAPI(title="Analista SemParar - V1")

# Caminho dentro do container (conforme definido no docker-compose)
DB_PATH = "/var/abastece/dados/abastece.db"

@app.get("/")
def home():
    return {"status": "Online", "projeto": "Analista SemParar"}

@app.get("/transacoes")
def listar_transacoes():
    if not os.path.exists(DB_PATH):
        raise HTTPException(status_code=404, detail="Banco de dados não encontrado")
    
    try:
        conn = sqlite3.connect(DB_PATH)
        # Permite acessar as colunas pelo nome (ex: row['valor'])
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM transacoes ORDER BY timestamp DESC")
        rows = cursor.fetchall()
        
        # Converte os resultados para uma lista de dicionários
        resultado = [dict(row) for row in rows]
        
        conn.close()
        return {"total": len(resultado), "dados": resultado}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao ler banco: {str(e)}")

@app.get("/health")
def health_check():
    return {"status": "healthy", "db_connected": os.path.exists(DB_PATH)}