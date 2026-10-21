import os

# Valores sensíveis externalizados via variáveis de ambiente (SEC-24).
# Sem a variável setada, cai no fallback (comportamento atual preservado).
CONVENIADO_CODE = os.environ.get("CONVENIADO_CODE", "02896")
SFTP_SERVER = os.environ.get("SFTP_SERVER", "DS_ABAST.02896_1")
NUC_IP = os.environ.get("NUC_IP", "192.168.212.21")

VALIDACOES = [
    {
        "dado": "codigoConveniado",
        "valor": CONVENIADO_CODE,
        "checks": [
            {"arquivo": "/etc/abastece/lado1/posto.json", "tipo": "json_valor", "chave": "postoId"},
            {"arquivo": "/etc/abastece/lado2/posto.json", "tipo": "json_valor", "chave": "postoId"},
            {"arquivo": "/var/abastece/SLT/configpista/ifadapter.ini", "tipo": "texto", "padrao": CONVENIADO_CODE},
        ]
    },
    {
        "dado": "config",
        "valor": SFTP_SERVER,
        "checks": [
            {"arquivo": "/var/DS_SFTP/config.json", "tipo": "json_valor", "chave": "server"},
        ]
    },
    {
        "dado": "IPs nuc",
        "valor": NUC_IP,
        "checks": [
            {"arquivo": "/etc/abastece/autorizador/retrofit-autorizador.json", "tipo": "json_busca"},
            {"arquivo": "/etc/abastece/lado1/antena.json", "tipo": "json_busca"},
            {"arquivo": "/etc/abastece/lado2/antena.json", "tipo": "json_busca"},
            {"arquivo": "/etc/abastece/lado1/camera.json", "tipo": "json_busca"},
            {"arquivo": "/etc/abastece/lado1/camera.json", "tipo": "json_busca"},
            {"arquivo": "/etc/abastece/lado1/camera.json", "tipo": "json_busca"},
            {"arquivo": "/etc/abastece/lado2/camera.json", "tipo": "json_busca"},
            {"arquivo": "/etc/abastece/lado2/camera.json", "tipo": "json_busca"},
            {"arquivo": "/etc/abastece/lado2/camera.json", "tipo": "json_busca"},
        ]
    },
    {
        "dado": "lane",
        "valor": "1 / 2",
        "checks": [
            {"arquivo": "/etc/abastece/lado1/antena.json", "tipo": "json_valor", "chave": "lane", "valor_esperado": "1"},
            {"arquivo": "/etc/abastece/lado2/antena.json", "tipo": "json_valor", "chave": "lane", "valor_esperado": "2"},
            {"arquivo": "/etc/abastece/lado1/posto.json", "tipo": "json_valor", "chave": "pista", "valor_esperado": "1"},
            {"arquivo": "/etc/abastece/lado2/posto.json", "tipo": "json_valor", "chave": "pista", "valor_esperado": "2"},
        ]
    },
    {
        "dado": "Portas Antena",
        "valor": "51111",
        "checks": [
            {"arquivo": "/etc/abastece/lado1/antena.json", "tipo": "json_valor", "chave": "porta"},
            {"arquivo": "/etc/abastece/lado2/antena.json", "tipo": "json_valor", "chave": "porta"},
        ]
    },
    {
        "dado": "Portas Camera",
        "valor": "50041/50042",
        "checks": [
            {"arquivo": "/etc/abastece/lado1/camera.json", "tipo": "json_valor", "chave": "porta", "valor_esperado": "50041"},
            {"arquivo": "/etc/abastece/lado2/camera.json", "tipo": "json_valor", "chave": "porta", "valor_esperado": "50042"},
        ]
    },
    {
        "dado": "wtmp",
        "valor": "7",
        "checks": [
            {"arquivo": "/etc/logrotate.d/wtmp", "tipo": "texto", "padrao": "monthly"},
            {"arquivo": "/etc/logrotate.d/wtmp", "tipo": "texto", "padrao": "daily"},
            {"arquivo": "/etc/logrotate.d/wtmp", "tipo": "texto", "padrao": "rotate 1"},
            {"arquivo": "/etc/logrotate.d/wtmp", "tipo": "texto", "padrao": "rotate 7"},
        ]
    },
    {
        "dado": "zabbix",
        "valor": "ativado",
        "checks": [
            # O conf do agente é INI, não JSON (#79): validado como "json_valor"
            # devolvia json_invalido e a categoria nunca ficava ok. O tipo
            # "texto" devolve a linha que casa com o padrão — mesmo princípio
            # da categoria "wtmp" acima.
            {"arquivo": "/etc/zabbix/zabbix_agent2.conf", "tipo": "texto", "padrao": "Server="},
        ]
    },
]
