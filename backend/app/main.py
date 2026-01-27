from fastapi import FastAPI

app = FastAPI(title="Analista SemParar - V1")

@app.get("/")
def home():
    return {
        "status": "Online",
        "mensagem": "Motor de Análise do Analista SemParar iniciado com sucesso!",
        "v1": "MVP"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}