"""#63 — contrato de resolucao da variavel API_KEY.

Os testes de `test_seguranca.py` fazem patch de `app.main._API_KEY`, entao
nao provam a parte que quebrou o ambiente de estudo: **como a variavel de
ambiente vira o valor lido pelo modulo**.

O defeito original era um fallback com valor fixo — `API_KEY` ausente
produzia "dev-key-not-secure", ou seja, a variavel nunca ficava ausente e
o middleware nunca ficava inativo.

Aqui a prova e feita em **subprocesso**: importar `app.main` de novo no
mesmo processo registraria middleware repetido no app global.
"""

import os
import subprocess
import sys
from pathlib import Path

BACKEND = Path(__file__).resolve().parents[1]


def _resolver_api_key(env_extra):
    """Importa app.main num processo limpo e devolve o _API_KEY resolvido."""
    env = {k: v for k, v in os.environ.items() if k != "API_KEY"}
    env.update(env_extra)
    env["PYTHONPATH"] = str(BACKEND)

    proc = subprocess.run(
        [
            sys.executable,
            "-c",
            "from app.main import _API_KEY; print(repr(_API_KEY))",
        ],
        capture_output=True,
        text=True,
        env=env,
        cwd=str(BACKEND),
        timeout=60,
    )
    assert proc.returncode == 0, f"import falhou: {proc.stderr}"
    return proc.stdout.strip()


def test_api_key_ausente_resolve_vazio():
    """Sem a variavel, o valor precisa ser vazio — nao um fallback fixo."""
    assert _resolver_api_key({}) == "''"


def test_api_key_vazia_resolve_vazio():
    assert _resolver_api_key({"API_KEY": ""}) == "''"


def test_api_key_so_espacos_resolve_vazio():
    """Espaco em branco nao deve virar credencial de grau nenhum."""
    assert _resolver_api_key({"API_KEY": "   "}) == "''"


def test_api_key_presente_e_respeitada():
    assert _resolver_api_key({"API_KEY": "segreda-de-teste"}) == "'segreda-de-teste'"


def test_api_key_presente_e_cortada():
    """Espaco nas pontas e trimmed, para nao quebrar a comparacao."""
    assert _resolver_api_key({"API_KEY": "  segredo-de-teste  "}) == "'segredo-de-teste'"
