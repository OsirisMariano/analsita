"""#81 — o card "Vendas Hoje" só pode contar o dia de hoje.

O PRD §6 (FR-02) pede o *total de vendas do dia*. A implementação somava
o banco inteiro: o card dizia "Vendas Hoje" e mostrava a soma de tudo que
estivesse gravado, inclusive de meses atrás. Com o banco de referência o
problema é invisível (as transações são de hoje), mas com dados antigos o
card mente — e o FR-02 estava marcado "✅ Conforme" na auditoria da §11.6
só porque o endpoint existia.

O recorte é por **dia civil no fuso do servidor**, e vale só para a
agregação (o valor e as contagens do card). A tabela "5 últimas
transações" **não** é filtrada: ela mostra as mais recentes de qualquer
dia, que é o que o AC do §10 promete ("Últimas 5 transações").

A prova aqui é feita num banco temporário, criado pelo próprio teste, para
não depender do banco do ambiente. As datas são **relativas** — fixar uma
data no teste faria o próprio teste depender do dia em que roda.
"""

import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from app import main
from app.main import app

from unittest import mock

# Mesmo schema do scripts/simulador_posto.py
SCHEMA = """
CREATE TABLE transacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME,
    pista INTEGER,
    veiculo_tag TEXT,
    valor REAL,
    status TEXT
)
"""


def _em(dias=0, hora=12):
    """Um instante dentro do dia desejado.

    Fica no meio-dia de propósito: perto da meia-noite, um "hoje às 00:00"
    poderia cair no dia anterior depending de quando o teste roda.
    """
    base = datetime.now().replace(hour=hora, minute=0, second=0, microsecond=0)
    return str(base - timedelta(days=dias))


@pytest.fixture()
def client():
    """Cliente sem o ping real dos equipamentos (deixa o teste rápido)."""
    with mock.patch("app.main.obter_status_pista") as fake:
        fake.return_value = []
        with TestClient(app) as c:
            yield c


def _banco_com(client, transacoes, tmp_path, monkeypatch):
    """Aponta a aplicação para um banco novo com as transações dadas."""
    caminho = tmp_path / "abastece.db"
    conn = sqlite3.connect(caminho)
    conn.execute(SCHEMA)
    conn.executemany(
        "INSERT INTO transacoes (timestamp, pista, veiculo_tag, valor, status)"
        " VALUES (?, 1, 'TAG-1001', ?, ?)",
        transacoes,
    )
    conn.commit()
    conn.close()
    monkeypatch.setattr(main, "DB_PATH", str(caminho))
    return client


def test_agregado_conta_somente_o_dia_de_hoje(client, tmp_path, monkeypatch):
    """A agregação do card olha para um dia só."""
    _banco_com(
        client,
        [
            (_em(dias=0), 100.00, "CONCLUIDO"),
            (_em(dias=0), 50.00, "FALHA"),
            (_em(dias=1), 999.00, "CONCLUIDO"),
            (_em(dias=30), 555.00, "CONCLUIDO"),
        ],
        tmp_path,
        monkeypatch,
    )

    transacoes = client.get("/stats").json()["transacoes"]

    assert transacoes["concluidas"] == 1
    assert transacoes["falhas"] == 1
    assert transacoes["valor_total"] == 100.00


def test_card_zera_quando_so_ha_transacoes_antigas(client, tmp_path, monkeypatch):
    """Um banco sem movimento hoje mostra zero — e não a soma do arquivo."""
    _banco_com(
        client,
        [
            (_em(dias=1), 999.00, "CONCLUIDO"),
            (_em(dias=30), 555.00, "CONCLUIDO"),
        ],
        tmp_path,
        monkeypatch,
    )

    transacoes = client.get("/stats").json()["transacoes"]

    assert transacoes["concluidas"] == 0
    assert transacoes["falhas"] == 0
    assert transacoes["valor_total"] == 0.0


def test_tabela_de_ultimas_nao_e_filtrada(client, tmp_path, monkeypatch):
    """A tabela mostra as mais recentes de qualquer dia.

    Este é o outro lado do contrato: filtrar a tabela esconderia do
    operador exatamente o que ele precisa ver — uma transação antiga que
    deu errado.
    """
    _banco_com(
        client,
        [
            (_em(dias=0), 10.00, "CONCLUIDO"),
            (_em(dias=1), 999.00, "FALHA"),
        ],
        tmp_path,
        monkeypatch,
    )

    lista = client.get("/stats").json()["transacoes"]["lista_detalhada"]

    assert len(lista) == 2
    assert any(t["valor"] == 999.00 and t["status"] == "FALHA" for t in lista)


def test_valor_soma_somente_concluido(client, tmp_path, monkeypatch):
    """A falha e o em-aberto entram nas contagens, mas não no valor."""
    _banco_com(
        client,
        [
            (_em(dias=0), 100.00, "CONCLUIDO"),
            (_em(dias=0), 50.00, "FALHA"),
            (_em(dias=0), 70.00, "EM_ABERTO"),
        ],
        tmp_path,
        monkeypatch,
    )

    transacoes = client.get("/stats").json()["transacoes"]

    assert transacoes["concluidas"] == 1
    assert transacoes["falhas"] == 1
    assert transacoes["valor_total"] == 100.00


def test_banco_sem_nenhuma_transacao(client, tmp_path, monkeypatch):
    """Banco vazio não quebra o card."""
    _banco_com(client, [], tmp_path, monkeypatch)

    resp = client.get("/stats")

    assert resp.status_code == 200
    assert resp.json()["transacoes"]["valor_total"] == 0.0
    assert resp.json()["transacoes"]["lista_detalhada"] == []


def test_contrato_do_json_nao_muda(client, tmp_path, monkeypatch):
    """A correção filtra os números — ela não mexe no formato da resposta."""
    _banco_com(client, [(_em(dias=0), 100.00, "CONCLUIDO")], tmp_path, monkeypatch)

    corpo = client.get("/stats").json()

    assert set(corpo) == {"monitoramento", "transacoes"}
    assert set(corpo["monitoramento"]) == {"online", "offline", "total"}
    assert set(corpo["transacoes"]) == {
        "concluidas",
        "falhas",
        "valor_total",
        "lista_detalhada",
    }
