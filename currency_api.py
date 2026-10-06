import requests


# ==========================================================
# MOEDAS DISPONÍVEIS
# ==========================================================

MENU_MOEDAS = {

    # Principais moedas
    "BRL-USD": "Dólar Americano",
    "BRL-EUR": "Euro",
    "BRL-GBP": "Libra Esterlina",
    "BRL-JPY": "Iene Japonês",
    "BRL-CHF": "Franco Suíço",
    "BRL-CAD": "Dólar Canadense",
    "BRL-AUD": "Dólar Australiano",
    "BRL-CNY": "Yuan Chinês",

    # América do Sul
    "BRL-ARS": "Peso Argentino",
    "BRL-CLP": "Peso Chileno",
    "BRL-COP": "Peso Colombiano",
    "BRL-PYG": "Guarani Paraguaio",
    "BRL-UYU": "Peso Uruguaio",
    "BRL-PEN": "Sol do Peru",
    "BRL-BOB": "Boliviano",
    "BRL-CRC": "Colón Costarriquenho",

    # América do Norte / Caribe
    "BRL-MXN": "Peso Mexicano",
    "BRL-PAB": "Balboa Panamenho",
    "BRL-BBD": "Dólar de Barbados",
    "BRL-BBD": "Dólar de Barbados",
    "BRL-JMD": "Dólar Jamaicano",
    "BRL-XCD": "Dólar do Caribe Oriental",

    # Europa
    "BRL-DKK": "Coroa Dinamarquesa",
    "BRL-NOK": "Coroa Norueguesa",
    "BRL-SEK": "Coroa Sueca",
    "BRL-ISK": "Coroa Islandesa",
    "BRL-PLN": "Zlóti Polonês",
    "BRL-CZK": "Coroa Checa",
    "BRL-HUF": "Florim Húngaro",
    "BRL-RON": "Leu Romeno",
    "BRL-RUB": "Rublo Russo",
    "BRL-RSD": "Dinar Sérvio",
    "BRL-TRY": "Nova Lira Turca",

    # Oriente Médio
    "BRL-AED": "Dirham dos Emirados",
    "BRL-BHD": "Dinar do Bahrein",
    "BRL-ILS": "Novo Shekel Israelense",
    "BRL-JOD": "Dinar Jordaniano",
    "BRL-KWD": "Dinar Kuwaitiano",
    "BRL-OMR": "Rial Omanense",
    "BRL-QAR": "Rial Catarense",
    "BRL-SAR": "Riyal Saudita",
    "BRL-LBP": "Libra Libanesa",

    # Ásia
    "BRL-HKD": "Dólar de Hong Kong",
    "BRL-SGD": "Dólar de Cingapura",
    "BRL-TWD": "Dólar Taiuanês",
    "BRL-KRW": "Won Sul-Coreano",
    "BRL-INR": "Rúpia Indiana",
    "BRL-IDR": "Rupia Indonésia",
    "BRL-LKR": "Rúpia de Sri Lanka",
    "BRL-NPR": "Rúpia Nepalesa",
    "BRL-PKR": "Rúpia Paquistanesa",
    "BRL-THB": "Baht Tailandês",
    "BRL-MYR": "Ringgit Malaio",
    "BRL-PHP": "Peso Filipino",

    # Oceania
    "BRL-NZD": "Dólar Neozelandês",

    # África
    "BRL-EGP": "Libra Egípcia",
    "BRL-KES": "Shilling Queniano",
    "BRL-MAD": "Dirham Marroquino",
    "BRL-NAD": "Dólar Namíbio",
    "BRL-ZAR": "Rand Sul-Africano",
    "BRL-XAF": "Franco CFA Central",
    "BRL-XOF": "Franco CFA Ocidental",

    # Outras moedas presentes na API
    "BRL-VEF": "Bolívar Venezuelano",
}


# ==========================================================
# CONSULTA À API
# ==========================================================

def consultar_moeda(moeda):
    """
    Consulta uma cotação na AwesomeAPI.

    Exemplo:
        consultar_moeda("BRL-USD")
    """

    url = f"https://economia.awesomeapi.com.br/json/last/{moeda}"

    try:

        resposta = requests.get(
            url,
            timeout=10
        )

        dados = resposta.json()

        if resposta.status_code == 200:

            return dados

        status_erro = dados.get(
            "status",
            resposta.status_code
        )

        codigo_erro = dados.get(
            "code",
            "Não informado"
        )

        mensagem = dados.get(
            "message",
            "Erro desconhecido"
        )

        raise Exception(
            f"Status: {status_erro} | "
            f"Código: {codigo_erro} | "
            f"Mensagem: {mensagem}"
        )

    except requests.exceptions.Timeout:

        raise Exception(
            "A API demorou muito para responder."
        )

    except requests.exceptions.RequestException as erro:

        raise Exception(
            f"Erro na requisição: {erro}"
        )

    except ValueError:

        raise Exception(
            "A API retornou uma resposta inválida."
        )


# ==========================================================
# TRATAMENTO DOS DADOS
# ==========================================================

def obter_cotacao(moeda):
    """
    Obtém e organiza os dados da cotação.
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

        "compra": float(
            dados_moeda.get("bid", 0)
        ),

        "venda": float(
            dados_moeda.get("ask", 0)
        ),

        "maxima": float(
            dados_moeda.get("high", 0)
        ),

        "minima": float(
            dados_moeda.get("low", 0)
        ),

        "variacao": float(
            dados_moeda.get("pctChange", 0)
        ),

        "data": dados_moeda.get(
            "create_date"
        ),
    }