VALIDACOES = [
    {
        "dado": "codigoConveniado",
        "valor": "02896",
        "checks": [
            {"arquivo": "/etc/abastece/lado1/posto.json", "tipo": "json_valor", "chave": "postoId"},
            {"arquivo": "/etc/abastece/lado2/posto.json", "tipo": "json_valor", "chave": "postoId"},
            {"arquivo": "/var/abastece/SLT/configpista/ifadapter.ini", "tipo": "texto", "padrao": "02896"},
        ]
    },
    {
        "dado": "config",
        "valor": "DS_ABAST.02896_1",
        "checks": [
            {"arquivo": "/var/DS_SFTP/config.json", "tipo": "json_valor", "chave": "server"},
        ]
    },
    {
        "dado": "IPs nuc",
        "valor": "192.168.212.21",
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
            {"arquivo": "/etc/zabbix/zabbix_agent2.conf", "tipo": "json_valor", "chave": "Server"},
        ]
    },
]
