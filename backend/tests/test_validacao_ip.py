"""SEC-06: disparar_ping so executa subprocess com IP sintaticamente valido."""

import sys
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.main import disparar_ping

ENTRADAS_INVALIDAS = [
    "8.8.8.999",            # octeto fora do range
    "300.1.1.1",            # octeto impossivel
    "google.com",           # hostname nao e IP
    "meu ip favorito",      # texto livre
    "",                     # vazio
    "8.8.8.8; rm -rf /",    # tentativa de injecao de comando
    "8.8.8.8 && whoami",    # outra variante de injecao
]


def test_entrada_invalida_retorna_erro_sem_subprocess():
    """IP invalido retorna 'Erro' e o subprocess NUNCA e chamado."""
    for ruim in ENTRADAS_INVALIDAS:
        with mock.patch("app.main.subprocess.run") as fake_run:
            assert disparar_ping(ruim) == "Erro", f"falhou para {ruim!r}"
            fake_run.assert_not_called()


def test_ip_valido_executa_ping_com_lista_de_argumentos():
    """IP valido chega ao ping como lista de args (sem shell)."""
    with mock.patch("app.main.subprocess.run") as fake_run:
        fake_run.return_value.returncode = 1  # host inacessivel
        resultado = disparar_ping("192.168.1.10")

    assert resultado == "Offline"
    fake_run.assert_called_once()
    comando = fake_run.call_args.args[0]
    assert comando == ["ping", "-c", "1", "-W", "1", "192.168.1.10"]


def test_ips_do_equipamento_sao_validos():
    """Sanidade: os IPs fixos do monitoramento passam no proprio portao."""
    import ipaddress

    from app.main import EQUIPAMENTOS

    for eq in EQUIPAMENTOS:
        ipaddress.ip_address(eq["ip"])  # levanta ValueError se invalido
