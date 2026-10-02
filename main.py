import requests


menu_moedas = """

=== Opções de Moedas para Consulta ===

Tradicionais:

USD-BRL (Dólar Americano)
EUR-BRL (Euro)
GBP-BRL (Libra Esterlina)
ARS-BRL (Peso Argentino)

Criptomoedas:

BTC-BRL (Bitcoin)
ETH-BRL (Ethereum)

=====================================

"""


def consultar_moeda(moeda):
    url = f"https://economia.awesomeapi.com.br/json/last/{moeda}"

    resposta = requests.get(url)
    erro = resposta.json()

    if resposta.status_code == 200:
        print("Deu certo.")
        print(resposta.json())
        return resposta.json()
    else:
        status_erro = resposta["status"]
        codigo_erro = resposta["code"]
        mensagem = resposta["message"]
        print(f"O seu status de erro foi {status_erro}, o código este {codigo_erro} e a mensagem é esta {mensagem}.")

moeda_desejada = input("Digite a moeda que deseja consultar (ex: USD-BRL): ")

dados_api = consultar_moeda(moeda_desejada)
#---------------------------------------tratamento de JSON-----------------------------------------------

if dados_api:
    valor = dados_api["JPYBRL"]["code"]["bid"]
    print("\nRequisição bem-sucedida!")

    print(f"O valor atual de {moeda_desejada} é: ")
    print(f"R$ {float(valor):.2f}")
else:
    print(f"\nErro ao consultar a moeda: {moeda_desejada} \nVerifique se o formato está correto.")
print(menu_moedas)