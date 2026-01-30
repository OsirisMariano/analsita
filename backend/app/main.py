from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os
import subprocess

# 1. Instância do App (Sempre antes das rotas)
app = FastAPI(title="Analista SemParar - V1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite requisições de qualquer origem (ideal para dev)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos os headers
)

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

@app.get("/stats")
def obter_resumo():
    resumo = {
        "monitoramento": {"online": 0, "offline": 0, "total": 0},
        "transacoes": {
            "concluidas": 0, 
            "falhas": 0, 
            "valor_total": 0.0,
            "lista_detalhada": []  # <--- Adicionamos o campo aqui
        }
    }
    
    for eq in EQUIPAMENTOS:
        status = disparar_ping(eq["ip"])
        resumo["monitoramento"]["total"] += 1
        if status == "Online":
            resumo["monitoramento"]["online"] += 1
        else:
            resumo["monitoramento"]["offline"] += 1

    if os.path.exists(DB_PATH):
        try:
            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row # Essencial para transformar em dicionário
            cursor = conn.cursor()
            
            # 1. Agregado financeiro
            cursor.execute("SELECT status, COUNT(*), SUM(valor) FROM transacoes GROUP BY status")
            rows = cursor.fetchall()
            for row in rows:
                status, qtd, soma_valor = row[0], row[1], row[2]
                if status == 'CONCLUIDO':
                    resumo["transacoes"]["concluidas"] = qtd
                    resumo["transacoes"]["valor_total"] = round(soma_valor or 0, 2)
                elif status == 'FALHA':
                    resumo["transacoes"]["falhas"] = qtd

            # 2. BUSCA AS ÚLTIMAS 5 TRANSAÇÕES (A correção que faltava!)
            cursor.execute("SELECT * FROM transacoes ORDER BY timestamp DESC LIMIT 5")
            ultimas = cursor.fetchall()
            resumo["transacoes"]["lista_detalhada"] = [dict(r) for r in ultimas]
            
            conn.close()
        except Exception as e:
            print(f"Erro ao agregar DB: {e}")

    return resumo