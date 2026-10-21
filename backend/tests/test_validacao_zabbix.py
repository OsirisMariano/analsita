"""#79: a categoria zabbix não pode mais falhar com json_invalido.

O conf do agente (`zabbix_agent2.conf`) é INI — `Server=...`, `Hostname=...` —,
não JSON. Validado como "json_valor" o json.loads falhava e a categoria ficava
sempre com erro, o que derrubava o status_geral da página de Validação de Dados.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import validador
from app.validacoes_config import VALIDACOES
from app.validador import validar_categoria

# Mesmo formato do mock versionado em mock_data/etc/zabbix/zabbix_agent2.conf
CONF_INI_ZABBIX = "Server=192.0.2.1\nHostname=posto-mock\n"


def _categoria_zabbix():
    return next(v for v in VALIDACOES if v["dado"] == "zabbix")


def _conf_em_tmp(tmp_path, monkeypatch, conteudo=CONF_INI_ZABBIX):
    """Escreve o conf num tmp e abre a whitelist só pra ele."""
    conf = tmp_path / "zabbix_agent2.conf"
    conf.write_text(conteudo, encoding="utf-8")
    monkeypatch.setattr(validador, "ALLOWED_PREFIXES", (str(tmp_path) + "/",))
    return conf


def _encontrar_mock():
    """Procura o conf versionado subindo a partir do teste e do diretório atual."""
    raizes = [Path(__file__).resolve().parents[2], Path.cwd(), *Path.cwd().parents]
    for raiz in raizes:
        candidato = raiz / "mock_data" / "etc" / "zabbix" / "zabbix_agent2.conf"
        if candidato.exists():
            return candidato
    return None


def test_regra_da_categoria_zabbix_le_o_conf_como_texto():
    """A regra tem de usar o tipo texto: o arquivo é INI, não JSON."""
    for check in _categoria_zabbix()["checks"]:
        assert check["tipo"] == "texto"
        assert "chave" not in check


def test_conf_ini_passa(tmp_path, monkeypatch):
    """Um conf em INI valida com status ok e devolve a linha do Server."""
    check = dict(_categoria_zabbix()["checks"][0])
    check["arquivo"] = str(_conf_em_tmp(tmp_path, monkeypatch))

    resultados = validar_categoria(
        {"dado": "zabbix", "valor": "ativado", "checks": [check]}
    )

    assert resultados[0]["status"] == "ok"
    assert "Server=" in resultados[0]["dado"]


def test_regra_antiga_json_valor_falha_no_conf_ini(tmp_path, monkeypatch):
    """Prova de que o teste pega a regressão: com a regra antiga (json_valor)
    o mesmo conf INI volta como json_invalido."""
    conf = _conf_em_tmp(tmp_path, monkeypatch)

    resultados = validar_categoria(
        {
            "dado": "zabbix",
            "valor": "ativado",
            "checks": [
                {"arquivo": str(conf), "tipo": "json_valor", "chave": "Server"}
            ],
        }
    )

    assert resultados[0]["status"] == "json_invalido"


def test_conf_do_mock_versionado_passa(tmp_path, monkeypatch):
    """O conf que realmente sobe no container valida com a regra da categoria."""
    mock = _encontrar_mock()
    if mock is None:
        pytest.skip("mock_data não está disponível neste ambiente")

    check = dict(_categoria_zabbix()["checks"][0])
    check["arquivo"] = str(_conf_em_tmp(tmp_path, monkeypatch, mock.read_text(encoding="utf-8")))

    resultados = validar_categoria(
        {"dado": "zabbix", "valor": "ativado", "checks": [check]}
    )

    assert resultados[0]["status"] == "ok"
