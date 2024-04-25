import requests
import json
import time

# URL da API onde os dados serão enviados
url = 'http://localhost:8000/api/'

def menu():
    return input("""
(1) Ver dispositivos disponíveis;
(2) Ligar sensor;
(3) Desligar sensor;   
(4) Solicitar medição atual do sensor;
(5) Adicionar dispositivo;
>>> """)

class Dispositivo():
    def __init__(self, id, tipo_medicao, medicao_atual, esta_ativo):
        self.id = id
        self.tipo_medicao = tipo_medicao
        self.medicao_atual = medicao_atual
        self.esta_ativo = esta_ativo

def desserializacao(lista_json):
    dispositivos = []
    for objeto in lista_json:
        id = objeto["pk"]
        tipo_medicao = objeto["fields"]["tipo_medicao"]
        medicao_atual = objeto["fields"]["medicao_atual"]
        esta_ativo = objeto["fields"]["esta_ativo"]
        dispositivo = Dispositivo(id, tipo_medicao, medicao_atual, esta_ativo)
        dispositivos.append(dispositivo)
    return dispositivos


def ver_todos_dispositivos():
    response = requests.get(url)
    response = eval(json.loads(response.text).replace("true", "True").replace("null", "None").replace("false", "False"))
    lista_dispositivos = desserializacao((response))
    print()
    for item in lista_dispositivos:
        esta_ativo = '\033[92m Está ligado. \033[0m' if item.esta_ativo else '\033[91m Está desligado. \033[0m'
        print("ID: " + str(item.id) + " - Tipo de Medição: " + item.tipo_medicao + " - " + esta_ativo)

while True:
    opcao = menu()
    try:
        if opcao == "1":
            ver_todos_dispositivos()
        elif opcao == "2":
            id = input("Informe qual o ID do dispositivo desejado: ")
            response = requests.post(url, data={"id": id, "comando": "ligar"})
            response = eval(response.content)
            if (response["value"] == "ligado"):
                print(f"\nDispositivo ligado!")
            else:
                print(f"Erro: {response}")
        elif opcao == "3":
            id = input("Informe qual o ID do dispositivo desejado: ")
            response = requests.post(url, data={"id": id, "comando": "desligar"})
            response = eval(response.content)
            if (response["value"] == "desligado"):
                print(f"\nDispositivo desligado!")
            else:
                print(f"Erro: {response}")
        elif opcao == "4":
            id = input("Informe qual o ID do dispositivo desejado: ")
            response = requests.post(url, data={"id": id, "comando": "dados"})
            response = eval(response.content)
            if 'value' in response:
                print(f"\nMedição atual: {response['value']}")
            else:
                print(response)
        elif opcao == "5":
            tipo_medicao = input("Informe o tipo de medição que o dispositivo faz: ")
            print("Conecte o novo dispositivo na tomada.")
            response = requests.post(url, data={"tipo_medicao": tipo_medicao, "comando": "adicionar_dispositivo"})
            response = eval(response.content)
            print("RESPONSE: ", response)
            if ('value' in response) and (response['value'] == 'dispositivo salvo'):
                print("Dispositivo salvo no Broker.")
            else:
                print("Dispositivo não foi salvo no Broker.")





        
        
        
    except requests.exceptions.ConnectionError:
        input("Verifique se o servidor está rodando e aperte enter.")

