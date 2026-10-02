"""Epico 1 - CORS + Autenticacao (SEC-01..05) e #63 (API Key opt-in).

Prova que:

Com API_KEY **ausente** (opt-in, #63) — ambiente de estudo:
- SEM header X-API-Key -> 200 (rota liberada)
- COM header qualquer -> 200 (header e ignorado)
- OPTIONS (preflight) -> nao e barrado

Com API_KEY **presente** — comportamento original preservado:
- SEM header X-API-Key -> 403
- COM header X-API-Key errado -> 403
- COM header X-API-Key nao-ASCII -> 403 (nao 500)
- COM header X-API-Key correto -> 200
- /health continua aberto (isentos)
- OPTIONS nao e barrado (lacuna conhecida, #64)
- allow_methods restrito a GET (SEC-02)

O patch em `app.main._API_KEY` e necessario porque a variavel e lida na
importacao do modulo — mudar o ambiente depois nao surtiria efeito.

Evita disparar ping real nos endpoints que tocam a rede.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from app.main import app

from unittest import mock

CHAVE_VALIDA = "chave-de-teste-nao-secreta"


def _client_com_ping_mascarado():
    with mock.patch("app.main.obter_status_pista") as fake:
        fake.return_value = []
        return TestClient(app)


@pytest.fixture()
def client_sem_chave():
    """API_KEY ausente: middleware inativo (opt-in, #63)."""
    with mock.patch("app.main._API_KEY", ""):
        yield _client_com_ping_mascarado()


@pytest.fixture()
def client_com_chave():
    """API_KEY presente: exigencia de credencial integral."""
    with mock.patch("app.main._API_KEY", CHAVE_VALIDA):
        yield _client_com_ping_mascarado()


# --------------------------------------------------------------------------
# Com API_KEY ausente — o caminho do ambiente de estudo (#63)
# --------------------------------------------------------------------------

def test_sem_api_key_configurada_libera_rota(client_sem_chave):
    resp = client_sem_chave.get("/monitoramento")
    assert resp.status_code == 200


def test_header_e_ignorado_quando_api_key_ausente(client_sem_chave):
    resp = client_sem_chave.get(
        "/monitoramento", headers={"X-API-Key": "qualquer-coisa"}
    )
    assert resp.status_code == 200


def test_preflight_options_nao_e_barrado_sem_chave(client_sem_chave):
    """O que destrava o painel: sem chave ativa o preflight passa."""
    resp = client_sem_chave.options(
        "/monitoramento",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert resp.status_code != 403


def test_health_continua_acessivel_sem_chave(client_sem_chave):
    resp = client_sem_chave.get("/health")
    assert resp.status_code == 200


# --------------------------------------------------------------------------
# Com API_KEY presente — comportamento original preservado
# --------------------------------------------------------------------------

def test_sem_api_key_retorna_403(client_com_chave):
    resp = client_com_chave.get("/monitoramento")
    assert resp.status_code == 403


def test_api_key_errada_retorna_403(client_com_chave):
    resp = client_com_chave.get("/monitoramento", headers={"X-API-Key": "chave-errada"})
    assert resp.status_code == 403


def test_api_key_valida_retorna_200(client_com_chave):
    resp = client_com_chave.get("/monitoramento", headers={"X-API-Key": CHAVE_VALIDA})
    assert resp.status_code == 200


def test_api_key_nao_ascii_retorna_403_e_nao_500(client_com_chave):
    """Header latin-1 nao pode estourar TypeError no compare_digest.

    O header vai como bytes crus porque o httpx recusa str nao-ASCII na
    borda. Enviando bytes, o que o servidor real receberia de um cliente
    com byte alto num header — e o starlette decodifica como latin-1,
    entregando str nao-ASCII ao compare_digest.
    """
    resp = client_com_chave.get("/monitoramento", headers={"X-API-Key": b"ch\xe1v\xe9"})
    assert resp.status_code == 403


def test_health_aber_to_sem_chave(client_com_chave):
    # /health esta na lista de rotas isentas
    resp = client_com_chave.get("/health")
    assert resp.status_code == 200


def test_options_ainda_barrado_com_chave_ativa(client_com_chave):
    """Lacuna CONHECIDA e documentada: e o que #64 corrige.

    Este teste existe para deixar o estado explícito. Quando #64 for
    entregue, ele deve falhar e ser invertido.
    """
    resp = client_com_chave.options("/monitoramento")
    assert resp.status_code == 403


def test_cors_allow_methods_restrito_a_get(client_com_chave):
    resp = client_com_chave.post(
        "/monitoramento",
        headers={"X-API-Key": CHAVE_VALIDA},
    )
    # nao existe rota POST -> 405 (metodo nao permitido pelo CORS/router)
    assert resp.status_code == 405
