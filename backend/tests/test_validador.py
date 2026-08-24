"""SEC-09: provas de que a whitelist bloqueia path traversal e que as
categorias legitimas (wtmp/zabbix/logrotate) continuam funcionando."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import validador
from app.validador import extrair_valor, validar_categoria

REGRA_TEXTO = {"tipo": "texto", "padrao": "x"}

# Tentaivas classicas de traversal: relativas, absolutas e disfarcadas
# com prefixo permitido (normpath resolve antes da conferencia).
PATHS_MALICIOSOS = [
    "../../etc/shadow",
    "/etc/shadow",
    "/etc/passwd",
    "/etc/abastece/../../etc/shadow",
    "/var/abastece/../../../../etc/shadow",
    "/etc/zabbix/../../../etc/shadow",
    "file:///etc/shadow",
]


@pytest.mark.parametrize("caminho", PATHS_MALICIOSOS)
def test_recusa_path_malicioso(caminho):
    """Path fora da whitelist retorna erro generico, sem tocar no FS."""
    valor, status = extrair_valor(caminho, REGRA_TEXTO)
    assert status == "acesso_nao_permitido"
    assert valor is None


def test_whitelist_tem_os_5_prefixos_da_emenda():
    assert len(validador.ALLOWED_PREFIXES) == 5
    for prefixo in (
        "/etc/abastece/",
        "/var/abastece/",
        "/var/DS_SFTP/",
        "/etc/zabbix/",
        "/etc/logrotate.d/",
    ):
        assert prefixo in validador.ALLOWED_PREFIXES


def test_arquivo_legitimo_continua_sendo_lido(tmp_path, monkeypatch):
    """Whitelist nao virou bloqueio total: prefixo permitido le normal."""
    arquivo = tmp_path / "agente.conf"
    arquivo.write_text("Server=127.0.0.1\n", encoding="utf-8")
    monkeypatch.setattr(validador, "ALLOWED_PREFIXES", (str(tmp_path) + "/",))

    valor, status = extrair_valor(
        str(arquivo), {"tipo": "texto", "padrao": "Server="}
    )
    assert status == "ok"
    assert "Server=127.0.0.1" in valor


def test_categoria_zabbix_sobrevive_a_regra_venenosa(tmp_path, monkeypatch):
    """Gate do merge: um check com path malicioso nao derruba a categoria;
    ele volta como erro generico isolado enquanto os checks legitimos seguem ok."""
    pasta_legitima = tmp_path / "zabbix"
    pasta_legitima.mkdir()
    (pasta_legitima / "agente.conf").write_text(
        "Server=127.0.0.1\n", encoding="utf-8"
    )
    monkeypatch.setattr(
        validador, "ALLOWED_PREFIXES", (str(pasta_legitima) + "/",)
    )

    validacao = {
        "dado": "zabbix agent",
        "valor": "Server=127.0.0.1",
        "checks": [
            {
                "arquivo": str(pasta_legitima / "agente.conf"),
                "tipo": "texto",
                "padrao": "Server=",
            },
            {   # regra venenosa injetada na config
                "arquivo": "../../etc/shadow",
                "tipo": "texto",
                "padrao": "root",
            },
        ],
    }

    resultados = validar_categoria(validacao)
    assert resultados[0]["status"] == "ok"
    assert resultados[1]["status"] == "acesso_nao_permitido"
