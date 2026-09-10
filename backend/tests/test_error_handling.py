"""Epico 4 - Error Handling (SEC-18..21).

Prova que:
- /transacoes em erro retorna 500 generico, sem str(e) no body
- /validacao-dados em erro retorna 500 generico, sem str(e) no body
- extrair_valor em erro de I/O retorna "erro_leitura" sem detalhe da excecao
"""

import sys
import builtins
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from app.main import app

from unittest import mock

from app.validador import extrair_valor

CHAVE_VALIDA = "dev-key-not-secure"

MSGS_GENERICAS = [
    "Erro interno ao acessar o banco de dados",
    "Erro interno ao processar a validação de dados",
]


@pytest.fixture()
def client():
    with mock.patch("app.main.obter_status_pista") as fake:
        fake.return_value = []
        with TestClient(app) as c:
            yield c


@mock.patch("app.main.os.path.exists", return_value=True)
def test_transacoes_erro_nao_vaza_excecao(_exists, client):
    with mock.patch(
        "sqlite3.connect", side_effect=RuntimeError("segredo interno")
    ):
        resp = client.get("/transacoes", headers={"X-API-Key": CHAVE_VALIDA})
    assert resp.status_code == 500
    assert MSGS_GENERICAS[0] in resp.text
    assert "segredo interno" not in resp.text


def test_validacao_dados_erro_nao_vaza_excecao(client):
    with mock.patch(
        "app.main.validar_categoria",
        side_effect=RuntimeError("detalhe da raiz"),
    ):
        resp = client.get("/validacao-dados", headers={"X-API-Key": CHAVE_VALIDA})
    assert resp.status_code == 500
    assert MSGS_GENERICAS[1] in resp.text
    assert "detalhe da raiz" not in resp.text


def test_erro_leitura_sem_detalhe(monkeypatch):
    """SEC-20: erro de I/O vira 'erro_leitura' puro, detalhe so no print()."""

    def fail(arquivo, **kwargs):
        raise PermissionError("Permission denied: '/etc/abastece/fake'")

    monkeypatch.setattr("os.path.exists", lambda p: True)
    monkeypatch.setattr(builtins, "open", fail)

    valor, status = extrair_valor(
        "/etc/abastece/foo", {"tipo": "texto", "padrao": "x"}
    )
    assert status == "erro_leitura"
    assert valor is None
    assert "Permission denied" not in status