"""
PARA RECEBER O VALOR SERÁ ATRAVÉS DO TCP:
"""

import socket
import random
import time

HOST = '0.0.0.0'
UDP_PORT = 44444  # Porta para comunicação UDP - porta do broker
SENSOR_ID = 'sensor1'  # Identificador do sensor
MEU_IP = socket.gethostbyname(socket.gethostname())

def recebe_conexao(server): # ELE TEM QUE SEMPRE RECEBER -> PRECISA INICIAR O RECEBE CONEXÃO ANTES DO BROKER.
    conexao, client_addr = server.accept()
    data = conexao.recv(1024).decode()
    print(f"Dispositivo conectado: {client_addr}") # broker
    print(f'Dados recebidos: {data}')
    # lidar com os comandos. retornar o id_aplicacao junto com o dados em solicita conexao 
    conexao.close()

    return client_addr, data

def solicita_conexao(id_aplicacao, data, sock, SERVER_IP):
    data = f"{data}"
    sock.sendto(data.encode(), (SERVER_IP, UDP_PORT))
    print(f"Dados enviados: {data}")

def envia_porta_para_broker(server, SERVER_IP, TCP_PORT, NOME, MEDICAO):
    time.sleep(1)
    data = f"('{NOME}', '{MEDICAO}', {TCP_PORT}, '{MEU_IP}')" # format: (nome, medicao, porta, ip)  
    sock.sendto(data.encode(), (SERVER_IP, UDP_PORT))
    print(SERVER_IP, UDP_PORT, "enviado para broker")

def generate_temperature():
    return round(random.uniform(20, 30), 2)  # Simula temperatura entre 20°C e 30°C

if __name__ == '__main__':
    SERVER_IP = input("Qual o IP do servidor? >> ")
    TCP_PORT = int(input("Qual a porta desse dispositivo (01024-65535)? >> "))
    while TCP_PORT < 1024 or TCP_PORT > 65535:
        TCP_PORT = int(input("A porta precisa estar entre 0 e 65535. >> "))
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, TCP_PORT))
    server.listen(1) #Só escuta de um broker
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    entrada = input("Dispositivo já foi instalado no broker? (S/N)\n>> ")
    if entrada.lower() == "n":
        NOME = input("Qual o nome deste dispositivo? >> ")
        MEDICAO = input("Que tipo de medição este dispositivo faz? >> ")
        envia_porta_para_broker(server, SERVER_IP, TCP_PORT, NOME, MEDICAO)
    while True:
        print("Dispositivo Startado")
        broker_info = recebe_conexao(server)
        print(broker_info)
        temp = generate_temperature()
        solicita_conexao('teste', temp, sock, SERVER_IP)
        time.sleep(2)
    conexao.close()
    server.close()
    sock.close()

# FLUXO:
# ATIVA SERVIDOR TCP -> RECEBE SOLICITAÇÃO DO BROKER -> SOLICITA CONEXÃO -> RESPONDE A TEMPERATURA PARA O BROKER 
