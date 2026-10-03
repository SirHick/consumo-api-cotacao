import requests


MENU_MOEDAS = {
    "USD-BRL": "Dólar Americano",
    "EUR-BRL": "Euro",
    "GBP-BRL": "Libra Esterlina",
    "ARS-BRL": "Peso Argentino",
    "BTC-BRL": "Bitcoin",
    "ETH-BRL": "Ethereum",
}


def consultar_moeda(moeda):
    """
    Consulta a cotação de uma moeda na AwesomeAPI.

    Exemplo:
        consultar_moeda("USD-BRL")
    """

    url = f"https://economia.awesomeapi.com.br/json/last/{moeda}"

    try:
        resposta = requests.get(url, timeout=10)

        dados = resposta.json()

        if resposta.status_code == 200:
            return dados

        status_erro = dados.get("status", resposta.status_code)
        codigo_erro = dados.get("code", "Não informado")
        mensagem = dados.get("message", "Erro desconhecido")

        raise Exception(
            f"Status: {status_erro} | "
            f"Código: {codigo_erro} | "
            f"Mensagem: {mensagem}"
        )

    except requests.exceptions.Timeout:
        raise Exception("A API demorou muito para responder.")

    except requests.exceptions.RequestException as erro:
        raise Exception(f"Erro na requisição: {erro}")

    except ValueError:
        raise Exception("A API retornou uma resposta inválida.")


def obter_cotacao(moeda):
    """
    Extrai as informações principais da resposta da API.
    """

    dados = consultar_moeda(moeda)

    chave = moeda.replace("-", "")

    if chave not in dados:
        raise Exception(
            f"Não foi possível encontrar os dados para {moeda}."
        )

    dados_moeda = dados[chave]

    return {
        "codigo": dados_moeda.get("code"),
        "nome": dados_moeda.get("name"),
        "compra": float(dados_moeda.get("bid", 0)),
        "venda": float(dados_moeda.get("ask", 0)),
        "maxima": float(dados_moeda.get("high", 0)),
        "minima": float(dados_moeda.get("low", 0)),
        "variacao": float(dados_moeda.get("pctChange", 0)),
        "data": dados_moeda.get("create_date"),
    }