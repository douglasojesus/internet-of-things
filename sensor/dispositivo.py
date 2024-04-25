"""
PARA RECEBER O VALOR SERÁ ATRAVÉS DO TCP:
"""

import socket
import random
import time

HOST = '0.0.0.0'
SERVER_IP = '127.0.0.1' # IP do servidor
TCP_PORT = 12345  # Porta para comunicação TCP - porta do dispositivo
UDP_PORT = 54321  # Porta para comunicação UDP - porta do broker
SENSOR_ID = 'sensor1'  # Identificador do sensor
MEU_IP = '127.0.0.1'

def recebe_conexao(server): # ELE TEM QUE SEMPRE RECEBER -> PRECISA INICIAR O RECEBE CONEXÃO ANTES DO BROKER.
    conexao, client_addr = server.accept()
    data = conexao.recv(1024).decode()
    print(f"Dispositivo conectado: {client_addr}") # broker
    print(f'Dados recebidos: {data}')
    # lidar com os comandos. retornar o id_aplicacao junto com o dados em solicita conexao 
    conexao.close()

    return client_addr, data

def solicita_conexao(id_aplicacao, data, sock):
    data = f"{data}"
    sock.sendto(data.encode(), (SERVER_IP, UDP_PORT))
    print(f"Dados enviados: {data}")

def envia_porta_para_broker(server):
    while True:
        time.sleep(2)
        data = f"('{SENSOR_ID}', {TCP_PORT}, {MEU_IP})"
        sock.sendto(data.encode(), (SERVER_IP, UDP_PORT))
        recebido = recebe_conexao(server)
        print("oi")
        print(recebido)
        if recebido[1] == "recebido":
            break
    print("tudo ok")


def generate_temperature():
    return round(random.uniform(20, 30), 2)  # Simula temperatura entre 20°C e 30°C

if __name__ == '__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, TCP_PORT))
    server.listen(1) #Só escuta de um broker
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    entrada = int(input("1 - se dispositivo já foi instalado no broker.\n2 - se dispositivo vai ser instalado agora\n"))
    if entrada == 2:
        envia_porta_para_broker(server)
    while True:
        print("Dispositivo Startado")
        broker_info = recebe_conexao(server)
        print(broker_info)
        temp = generate_temperature()
        solicita_conexao('teste', temp, sock)
        time.sleep(2)
    conexao.close()
    server.close()
    sock.close()

# FLUXO:
# ATIVA SERVIDOR TCP -> RECEBE SOLICITAÇÃO DO BROKER -> SOLICITA CONEXÃO -> RESPONDE A TEMPERATURA PARA O BROKER 
