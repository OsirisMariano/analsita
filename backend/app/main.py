from fastapi import FastAPI, HTTPException
import sqlite3
import os
import subprocess

# 1. Instância do App (Sempre antes das rotas)
app = FastAPI(title="Analista SemParar - V1")

# 2. Configurações e Constantes
DB_PATH = "/var/abastece/dados/abastece.db"

EQUIPAMENTOS = [
    {"id": "antena_01", "ip": "192.168.1.10", "nome": "Antena Lado A"},
    {"id": "antena_02", "ip": "192.168.1.11", "nome": "Antena Lado B"},
    {"id": "sensor_vpar", "ip": "192.168.1.20", "nome": "Câmera VPAR"},
    {"id": "gateway", "ip": "8.8.8.8", "nome": "Saída Internet"} 
]

# 3. Funções Auxiliares
def disparar_ping(ip):
    try:
        # Executa o ping: -c 1 (1 pacote), -W 1 (espera 1 seg)
        comando = ["ping", "-c", "1", "-W", "1", ip]
        resultado = subprocess.run(comando, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return "Online" if resultado.returncode == 0 else "Offline"
    except Exception:
        return "Erro"

# 4. Rotas (Endpoints)
@app.get("/")
def home():
    return {"status": "Online", "projeto": "Analista SemParar"}

@app.get("/monitoramento")
def checar_rede():
    status_pista = []
    for eq in EQUIPAMENTOS:
        status = disparar_ping(eq["ip"])
        status_pista.append({
            "nome": eq["nome"],
            "ip": eq["ip"],
            "status": status
        })
    return {"dispositivos": status_pista}

@app.get("/transacoes")
def listar_transacoes():
    if not os.path.exists(DB_PATH):
        raise HTTPException(status_code=404, detail="Banco de dados não encontrado")
    
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transacoes ORDER BY timestamp DESC")
        rows = cursor.fetchall()
        resultado = [dict(row) for row in rows]
        conn.close()
        return {"total": len(resultado), "dados": resultado}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao ler banco: {str(e)}")

@app.get("/health")
def health_check():
    return {"status": "healthy", "db_connected": os.path.exists(DB_PATH)}