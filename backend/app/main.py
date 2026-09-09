from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import sqlite3
import os
import json
import subprocess
import time
import threading
import glob as glob_module
import ipaddress
import hmac
from concurrent.futures import ThreadPoolExecutor
from .arquivos_config import ARQUIVOS_CONFIG
from .validacoes_config import VALIDACOES
from .validador import validar_categoria

# 1. Instância do App (Sempre antes das rotas)
app = FastAPI(title="Analista SemParar - V1")

# SEC-01: origins restrito via CORS_ORIGINS (ex: "http://localhost:5173,http://10.0.0.1:5173")
_cors_origins_raw = os.environ.get("CORS_ORIGINS", "")
_cors_origins = [
    o.strip() for o in _cors_origins_raw.split(",") if o.strip()
] if _cors_origins_raw else ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=True,
    allow_methods=["GET"],  # SEC-02: apenas GET
    allow_headers=["X-API-Key"],
)

# SEC-04 / SEC-03: API_KEY via variável de ambiente
# Em desenvolvimento, usa um valor fixo para não bloquear o workflow.
_API_KEY = os.environ.get("API_KEY", "dev-key-not-secure")

# SEC-03: Middleware — exige header X-API-Key em todas as rotas exceto /health
Rotas_Isentas = {"/health", "/docs", "/openapi.json", "/redoc"}


class ApiKeyMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        if request.url.path in Rotas_Isentas:
            return await call_next(request)
        chave = request.headers.get("X-API-Key")
        if not chave or not hmac.compare_digest(chave, _API_KEY):
            return JSONResponse(
                content={"detail": "API key inválida ou ausente"},
                status_code=403,
            )
        return await call_next(request)


app.add_middleware(ApiKeyMiddleware)

# 2. Configurações e Constantes
DB_PATH = os.environ.get("DB_PATH", "/var/abastece/dados/abastece.db")

# EQUIPAMENTOS pode vir do ambiente como JSON (ex: [{"id":..., "ip":..., "nome":...}]).
# Se a variável não existir ou for um JSON inválido, usa o fallback abaixo.
_DEFAULT_EQUIPAMENTOS = [
    {"id": "antena_01", "ip": "192.168.1.10", "nome": "Antena Lado A"},
    {"id": "antena_02", "ip": "192.168.1.11", "nome": "Antena Lado B"},
    {"id": "sensor_vpar", "ip": "192.168.1.20", "nome": "Câmera VPAR"},
    {"id": "gateway", "ip": "8.8.8.8", "nome": "Saída Internet"} 
]

def _carregar_equipamentos():
    raw = os.environ.get("EQUIPAMENTOS", "")
    if not raw:
        return _DEFAULT_EQUIPAMENTOS
    try:
        dados = json.loads(raw)
    except json.JSONDecodeError:
        return _DEFAULT_EQUIPAMENTOS
    if not isinstance(dados, list):
        return _DEFAULT_EQUIPAMENTOS
    return dados

EQUIPAMENTOS = _carregar_equipamentos()

# 3. Funções Auxiliares
def disparar_ping(ip):
    try:
        # Portão de entrada (SEC-06): só executa subprocess se o input é
        # um IP sintaticamente válido — hostnames e injeções morrem aqui,
        # antes de chegar perto do sistema operacional.
        ipaddress.ip_address(ip)
    except ValueError:
        return "Erro"

    try:
        # Executa o ping: -c 1 (1 pacote), -W 1 (espera 1 seg)
        comando = ["ping", "-c", "1", "-W", "1", str(ip)]
        resultado = subprocess.run(comando, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return "Online" if resultado.returncode == 0 else "Offline"
    except Exception:
        return "Erro"

# Cache do status da pista: evita repetir os mesmos pings a cada requisição
CACHE_DURACAO = 4  # segundos
_status_cache = {"ts": 0.0, "resultado": []}
_status_lock = threading.Lock()

def _ping_equipamento(eq):
    return (eq, disparar_ping(eq["ip"]))

def obter_status_pista():
    # Pings disparados em paralelo e resultado compartilhado entre endpoints
    agora = time.monotonic()
    with _status_lock:
        if agora - _status_cache["ts"] < CACHE_DURACAO:
            return _status_cache["resultado"]
        with ThreadPoolExecutor(max_workers=len(EQUIPAMENTOS)) as executor:
            resultado = list(executor.map(_ping_equipamento, EQUIPAMENTOS))
        _status_cache["ts"] = agora
        _status_cache["resultado"] = resultado
        return resultado

# 4. Rotas (Endpoints)
@app.get("/")
def home():
    return {"status": "Online", "projeto": "Analista SemParar"}

@app.get("/monitoramento")
def checar_rede():
    return {"dispositivos": [
        {"nome": eq["nome"], "ip": eq["ip"], "status": status}
        for eq, status in obter_status_pista()
    ]}

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
    
    for eq, status in obter_status_pista():
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

@app.get("/arquivos")
def validar_arquivos():
    resultados = []
    for arq in ARQUIVOS_CONFIG:
        if "glob" in arq:
            padrao = os.path.join(arq["caminho"], arq["glob"])
            existe = len(glob_module.glob(padrao)) > 0
        else:
            existe = os.path.exists(arq["caminho"])
        resultados.append({
            "nome": arq["nome"],
            "caminho": arq["caminho"],
            "status": "OK" if existe else "ERRO"
        })
    total_erros = sum(1 for r in resultados if r["status"] == "ERRO")
    return {"arquivos": resultados, "total_erros": total_erros}

@app.get("/validacao-dados")
def validar_dados():
    validacoes_resultado = []
    for val in VALIDACOES:
        arquivos_resultado = validar_categoria(val)
        total = len(arquivos_resultado)
        erros = sum(1 for a in arquivos_resultado if a["status"] != "ok")

        validacoes_resultado.append({
            "dado": val["dado"],
            "valor": val["valor"],
            "total_arquivos": total,
            "status": "ok" if erros == 0 else f"{erros} erro(s)",
            "arquivos": arquivos_resultado
        })

    total_validacoes = sum(v["total_arquivos"] for v in validacoes_resultado)
    total_categorias_com_erro = sum(1 for v in validacoes_resultado if v["status"] != "ok")

    return {
        "arquivos_validados_total": total_validacoes,
        "status_geral": "sucesso" if total_categorias_com_erro == 0 else "erro",
        "validacoes": validacoes_resultado
    }