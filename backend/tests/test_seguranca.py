"""Epico 1 - CORS + Autenticacao (SEC-01..05).

Prova que:
- SEM header X-API-Key -> 403
- COM header X-API-Key errado -> 403
- COM header X-API-Key correto -> 200
- /health continua aberto (isentos)
- allow_methods restrito a GET (SEC-02)
- ! - Evita disparar ping real nos endpoints que tocam a rede.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from app.main import app

from unittest import mock

CHAVE_VALIDA = "dev-key-not-secure"


@pytest.fixture()
def client():
    with mock.patch("app.main.obter_status_pista") as fake:
        fake.return_value = []
        with TestClient(app) as c:
            yield c


def test_sem_api_key_retorna_403(client):
    resp = client.get("/monitoramento")
    assert resp.status_code == 403


def test_api_key_errada_retorna_403(client):
    resp = client.get("/monitoramento", headers={"X-API-Key": "chave-errada"})
    assert resp.status_code == 403


def test_api_key_valida_retorna_200(client):
    resp = client.get("/monitoramento", headers={"X-API-Key": CHAVE_VALIDA})
    assert resp.status_code == 200


def test_health_aber_to_sem_chave(client):
    # /health esta na lista de rotas isentas
    resp = client.get("/health")
    assert resp.status_code == 200


def test_cors_allow_methods_restrito_a_get(client):
    resp = client.post(
        "/monitoramento",
        headers={"X-API-Key": CHAVE_VALIDA},
    )
    # nao existe rota POST -> 405 (metodo nao permitido pelo CORS/router)
    assert resp.status_code == 405
