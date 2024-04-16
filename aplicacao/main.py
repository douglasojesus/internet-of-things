import requests

# URL da API onde os dados serão enviados
url = ''

def menu():
    valor = input("""
(1) Temperatura;
(2) Umidade;   
    """)
    if valor == '1':
        var = "Temperatura"
    elif valor == "2":
        var = "Umidade"
    return var


# Dados a serem enviados (por exemplo, temperatura ou umidade)
dados = {'valor': menu()}

# Enviar a requisição POST com os dados
response = requests.post(url, data=dados)

# Verificar se a requisição foi bem-sucedida
if response.status_code == 201:
    print('Dados enviados com sucesso!')
else:
    print('Erro ao enviar os dados:', response.status_code)
