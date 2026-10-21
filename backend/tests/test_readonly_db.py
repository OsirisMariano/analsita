"""#74 (T8) — o banco SQLite é aberto em modo somente-leitura.

O PRD §7 (RNF "Segurança | Acesso ao banco") exige que a API não escreva no
banco. Antes desta correção isso era só uma convenção do código: as rotas
faziam `SELECT`, mas nada impedia uma escrita acidental.

A garantia agora é do próprio motor do SQLite (`mode=ro` na URI), e não do
filesystem — o mount de `./data` continua gravável porque o `entrypoint.sh`
precisa criar o banco quando ele ainda não existe.

A prova aqui é feita num banco temporário, criado pelo próprio teste, para
não depender do banco do ambiente.
"""

import hashlib
import sqlite3
import sys
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


def _criar_banco(caminho):
    """Cria um banco com o schema do simulador e 3 transações."""
    conn = sqlite3.connect(caminho)
    conn.execute(SCHEMA)
    conn.executemany(
        "INSERT INTO transacoes (timestamp, pista, veiculo_tag, valor, status)"
        " VALUES (?, ?, ?, ?, ?)",
        [
            ("2026-10-21 10:00:00", 1, "TAG-1001", 100.50, "CONCLUIDO"),
            ("2026-10-21 10:01:00", 2, "TAG-1002", 200.00, "FALHA"),
            ("2026-10-21 10:02:00", 3, "TAG-1003", 300.25, "EM_ABERTO"),
        ],
    )
    conn.commit()
    conn.close()


def _impressao_digital(caminho):
    """Hash + data de modificação do arquivo — a prova de que ele não mudou."""
    arquivo = Path(caminho)
    return (
        hashlib.sha256(arquivo.read_bytes()).hexdigest(),
        arquivo.stat().st_mtime_ns,
    )


@pytest.fixture()
def banco(tmp_path, monkeypatch):
    """Banco temporário apontado como DB_PATH da aplicação."""
    caminho = tmp_path / "abastece.db"
    _criar_banco(caminho)
    monkeypatch.setattr(main, "DB_PATH", str(caminho))
    return caminho


@pytest.fixture()
def client():
    """Cliente sem o ping real dos equipamentos (deixa o teste rápido)."""
    with mock.patch("app.main.obter_status_pista") as fake:
        fake.return_value = []
        with TestClient(app) as c:
            yield c


def test_conexao_rejeita_escrita(banco):
    """A prova direta: escrever no banco pela conexão da API é recusado."""
    conn = main._abrir_banco_readonly()
    try:
        with pytest.raises(sqlite3.OperationalError) as erro:
            conn.execute(
                "INSERT INTO transacoes (timestamp, pista, veiculo_tag, valor, status)"
                " VALUES ('2026-10-21 11:00:00', 1, 'TAG-9999', 1.0, 'CONCLUIDO')"
            )
        assert "readonly" in str(erro.value).lower()
    finally:
        conn.close()


def test_api_nao_altera_o_banco(banco, client):
    """As rotas leem o banco — e o arquivo do banco sai intacto."""
    antes = _impressao_digital(banco)

    resp_transacoes = client.get("/transacoes")
    assert resp_transacoes.status_code == 200
    assert resp_transacoes.json()["total"] == 3

    resp_stats = client.get("/stats")
    assert resp_stats.status_code == 200
    assert resp_stats.json()["transacoes"]["concluidas"] == 1

    assert _impressao_digital(banco) == antes


def test_conexao_usa_uri_readonly(banco):
    """A URL usada tem o mode=ro — trava o contrato, não só o efeito."""
    caminho_esperado = Path(banco).resolve().as_uri() + "?mode=ro"

    with mock.patch("app.main.sqlite3.connect") as fake_connect:
        fake_connect.return_value = mock.MagicMock()
        main._abrir_banco_readonly()

    assert fake_connect.call_args.args[0] == caminho_esperado
    assert fake_connect.call_args.kwargs["uri"] is True
