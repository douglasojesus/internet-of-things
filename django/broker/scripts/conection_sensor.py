import socket
import random
import time

HOST = '0.0.0.0'
SERVER_IP = '127.0.0.1'  # IP do servidor
TCP_PORT = 12345  # Porta para comunicação TCP
UDP_PORT = 54321  # Porta para comunicação UDP
SENSOR_ID = 'sensor1'  # Identificador do sensor

def recebe_conexao(): # ELE TEM QUE SEMPRE RECEBER -> PRECISA INICIAR O RECEBE CONEXÃO ANTES DO DISPOSITIVO.
    global UDP_PORT
    server_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_udp.bind((HOST, UDP_PORT))
    print(f"Servidor UDP aguardando conexões em {UDP_PORT}")

    data, addr = server_udp.recvfrom(1024)
    print(f"Dados recebidos via UDP de {addr}: {data.decode()}")

def solicita_conexao():
    global SERVER_IP, TCP_PORT, SENSOR_ID
    while True:
        try:
            sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock_tcp.connect((SERVER_IP, TCP_PORT))
            data = f"DADOS DA REQUEST"
            sock_tcp.sendall(data.encode())
            print(f"Dados enviados via TCP: {data}")
            sock_tcp.close()
            time.sleep(5)  # Envia dados a cada 5 segundos
        except Exception as e:
            print(f"Erro ao enviar dados via TCP: {e}")
            time.sleep(5)

# FLUXO:
# ATIVA SERVIDOR UDP -> RECEBE REQUISIÇÃO -> SOLICITA CONEXÃO -> RECEBE CONEXÃO -> RESPONDE REQUISIÇÃO 