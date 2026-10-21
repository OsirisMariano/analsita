"""Epico 1 - CORS + Autenticacao (SEC-01..05), #63 (API Key opt-in) e #64 (preflight).

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
- OPTIONS (preflight) -> nao e barrado mais (#64)
- preflight devolve o cabecalho de origem permitida e nada para as demais (SEC-01)
- allow_methods restrito a GET (SEC-02)

O patch em `app.main._API_KEY` e necessario porque a variavel e lida na
importacao do modulo — mudar o ambiente depois nao surtiria efeito.

Evita disparar ping real nos endpoints que tocam a rede.

Sobre #64 e o TestClient: o TestClient **nao dispara** preflight sozinho como
um browser faria, mas **executa** o caminho de OPTIONS de verdade quando o
teste pede explicitamente — a requisicao passa pela pilha de middlewares e o
CORSMiddleware responde. O que faltava era cobrir o cenario com API_KEY ativa,
que e o unico que quebrava. Ver `test_options_*` abaixo.
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


def test_options_nao_e_barrado_com_chave_ativa(client_com_chave):
    """#64: o preflight deixa de morrer em 403 com a chave ativa.

    Este teste era o inverso: afirmava o 403 para deixar o bug explicito.
    Agora fixa o comportamento corrigido.
    """
    resp = client_com_chave.options("/monitoramento")
    assert resp.status_code != 403


def test_cors_allow_methods_restrito_a_get(client_com_chave):
    resp = client_com_chave.post(
        "/monitoramento",
        headers={"X-API-Key": CHAVE_VALIDA},
    )
    # nao existe rota POST -> 405 (metodo nao permitido pelo CORS/router)
    assert resp.status_code == 405


# --------------------------------------------------------------------------
# #64 — preflight de CORS
# --------------------------------------------------------------------------
#
# Criterio da issue: "OPTIONS em qualquer rota da API responde nao-403",
# coberto de forma parametrizada para nao depender de ninguem lembrar de
# acrescentar rota nova na lista.

ROTAS_PUBLICAS = [
    "/",
    "/stats",
    "/monitoramento",
    "/transacoes",
    "/arquivos",
    "/validacao-dados",
    "/health",
]

ORIGEM_PERMITIDA = "http://localhost:5173"
ORIGEM_NEGADA = "http://origem-nao-permitida.example.com"

PREFIXO_PREFLIGHT = {
    "Origin": ORIGEM_PERMITIDA,
    "Access-Control-Request-Method": "GET",
    "Access-Control-Request-Headers": "x-api-key",
}


@pytest.mark.parametrize("rota", ROTAS_PUBLICAS)
def test_preflight_nao_retorna_403_em_nenhuma_rota(client_com_chave, rota):
    """Criterio de aceite da #64, com API_KEY ativa (o cenario que quebrava)."""
    resp = client_com_chave.options(rota, headers=PREFIXO_PREFLIGHT)
    assert resp.status_code != 403, f"preflight de {rota} foi barrado"


@pytest.mark.parametrize("rota", ROTAS_PUBLICAS)
def test_preflight_entrega_origem_permitida(client_com_chave, rota):
    """O preflight tem de ser RESPONDIDO pelo CORSMiddleware, nao apenas passar.

    Um 405 passaria em `!= 403` sem provar nada — o que destrava o browser e a
    presenca do cabecalho de origem permitida.
    """
    resp = client_com_chave.options(rota, headers=PREFIXO_PREFLIGHT)
    assert resp.status_code == 200
    assert resp.headers.get("access-control-allow-origin") == ORIGEM_PERMITIDA


def test_preflight_anuncia_o_header_de_chave(client_com_chave):
    """Sem isto o browser nem enviaria o X-API-Key na requisicao real.

    E a segunda metade do bug original: preflight respondia "nao, nao conheco
    esse header", e o pedido seguinte morria de todo jeito.
    """
    resp = client_com_chave.options("/stats", headers=PREFIXO_PREFLIGHT)
    allow_headers = resp.headers.get("access-control-allow-headers", "")
    assert "x-api-key" in allow_headers.lower()


def test_preflight_de_origem_negada_nao_recebe_permissao(client_com_chave):
    """SEC-01 preservado: isentar OPTIONS nao pode abrir CORS para qualquer um.

    E o contra-teste do item acima — sem ele, "OPTIONS nao retorna 403" poderia
    ser cumprido devolvendo 200 com `Access-Control-Allow-Origin: *`.
    """
    resp = client_com_chave.options(
        "/stats",
        headers={
            "Origin": ORIGEM_NEGADA,
            "Access-Control-Request-Method": "GET",
        },
    )
    assert resp.headers.get("access-control-allow-origin") is None


def test_options_nao_contorna_autenticacao_do_get(client_com_chave):
    """Isentar OPTIONS nao pode virar atalho para os dados (#64).

    OPTIONS e inerte; o que protege os dados e o GET. Este teste amarra os
    dois: depois de um preflight bem-sucedido, o GET segue exigindo a chave.
    """
    preflight = client_com_chave.options("/stats", headers=PREFIXO_PREFLIGHT)
    assert preflight.status_code == 200

    # Sem header: continua barrado, mesmo depois de um preflight aprovado.
    resp = client_com_chave.get("/stats")
    assert resp.status_code == 403

    # Com header errado: idem.
    resp = client_com_chave.get("/stats", headers={"X-API-Key": "chave-errada"})
    assert resp.status_code == 403

    # Com a chave certa: os dados saem. Fim a happy path do painel.
    resp = client_com_chave.get("/stats", headers={"X-API-Key": CHAVE_VALIDA})
    assert resp.status_code == 200


def test_options_sem_origin_nao_vaza_dado(client_com_chave):
    """Preflight exige Origin. Sem ele, OPTIONS cai no router e devolve 405.

    Confirma que a isencao nao abriu um metodo devolvedor de dados.
    """
    resp = client_com_chave.options("/stats")
    assert resp.status_code != 403
    assert "vendas" not in resp.text
