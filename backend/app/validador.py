import json
import os


def extrair_valor(caminho, regra):
    """Lê arquivo e extrai valor conforme o tipo da regra."""
    if not os.path.exists(caminho):
        return None, "arquivo_nao_encontrado"

    try:
        conteudo = open(caminho, encoding="utf-8", errors="replace").read()
    except Exception as e:
        return None, f"erro_leitura: {e}"

    tipo = regra["tipo"]

    if tipo == "json_valor":
        try:
            dados = json.loads(conteudo)
            chave = regra["chave"]
            valor = dados.get(chave)
            if valor is not None:
                return str(valor), "ok"
            return None, "chave_nao_encontrada"
        except json.JSONDecodeError:
            return None, "json_invalido"

    elif tipo == "json_busca":
        return conteudo, "ok"

    elif tipo == "texto":
        for linha in conteudo.splitlines():
            if regra["padrao"] in linha:
                return linha.strip(), "ok"
        return None, "padrao_nao_encontrado"

    return None, "tipo_desconhecido"


def validar_categoria(validacao):
    """Valida uma categoria completa e retorna o resultado."""
    resultados = []
    for check in validacao["checks"]:
        conteudo, status = extrair_valor(check["arquivo"], check)
        valor_encontrado = ""

        if status == "ok":
            if check["tipo"] == "json_busca":
                if validacao["valor"] in str(conteudo):
                    valor_encontrado = validacao["valor"]
                else:
                    status = "valor_nao_encontrado"
                    valor_encontrado = ""
            elif check["tipo"] == "json_valor":
                valor_encontrado = str(conteudo)
                valor_esperado = check.get("valor_esperado")
                if valor_esperado and valor_encontrado != valor_esperado:
                    status = "valor_incorreto"
            else:
                valor_encontrado = str(conteudo)

        resultados.append({
            "caminho_arquivo": check["arquivo"],
            "dado": valor_encontrado,
            "status": "ok" if status == "ok" else status
        })

    return resultados
