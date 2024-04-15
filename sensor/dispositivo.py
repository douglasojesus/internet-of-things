"""
PARA RECEBER O VALOR SERÁ ATRAVÉS DO TCP:
"""

import socket
import random
import time

HOST = '0.0.0.0'
SERVER_IP = '' # IP do servidor
TCP_PORT = 12345  # Porta para comunicação TCP
UDP_PORT = 54321  # Porta para comunicação UDP
SENSOR_ID = 'sensor1'  # Identificador do sensor

def recebe_conexao(): # ELE TEM QUE SEMPRE RECEBER -> PRECISA INICIAR O RECEBE CONEXÃO ANTES DO BROKER.
    global HOST, TCP_PORT
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, TCP_PORT))
    server.listen(1) #Só escuta de um broker
    conexao, client_addr = server.accept()
    data = conexao.recv(1024).decode()
    print(f"Dispositivo conectado: {client_addr}") # broker
    print(f'Dados: {data}')
    # lidar com os comandos. retornar o id_aplicacao junto com o dados em solicita conexao 
    conexao.close()
    server.close()
    return client_addr, data

def solicita_conexao(id_aplicacao, data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = f"{id_aplicacao} - {data}"
    sock.sendto(data.encode(), (SERVER_IP, UDP_PORT))
    print(f"Dados enviados: {data}")
    time.sleep(5)  # Envia dados a cada 5 segundos
    sock.close()

def generate_temperature():
    return round(random.uniform(20, 30), 2)  # Simula temperatura entre 20°C e 30°C

if __name__ == '__main__':
    while True:
        print("Dispositivo Startado")
        broker_info = recebe_conexao()
        print(broker_info)
        temp = generate_temperature()
        solicita_conexao('teste', temp)
        time.sleep(5)

# FLUXO:
# ATIVA SERVIDOR TCP -> RECEBE SOLICITAÇÃO DO BROKER -> SOLICITA CONEXÃO -> RESPONDE A TEMPERATURA PARA O BROKER 
