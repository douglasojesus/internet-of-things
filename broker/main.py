"""
O broker escuta em todas as interfaces ('0.0.0.0') na porta 9999.
Utilizamos um dicionário dispositivos para armazenar as conexões dos dispositivos.
A função handle_client é responsável por receber mensagens de um dispositivo e encaminhá-las 
para todos os outros dispositivos conectados.
A função main cria o socket do broker, aceita novas conexões e inicia uma thread para cada 
dispositivo conectado.
"""

import socket
import threading

# Configurações do broker
HOST = '0.0.0.0'  # Escuta em todas as interfaces
PORT = 9999  # Porta do broker

# Dicionário para armazenar as conexões dos dispositivos
dispositivos = {}

# Função para lidar com as conexões dos dispositivos
def handle_client(dispositivo_socket):
    while True:
        try:
            # Recebe dados do dispositivo
            data = dispositivo_socket.recv(1024)
            if not data:
                print(f"dispositivo desconectado: {dispositivos[dispositivo_socket]}")
                del dispositivos[dispositivo_socket]
                break

            # Encaminha a mensagem para todos os dispositivos conectados (exceto o remetente)
            for client in dispositivos:
                if client != dispositivo_socket:
                    client.send(data)
        except:
            print(f"Erro ao lidar com dispositivo: {dispositivos[dispositivo_socket]}")
            del dispositivos[dispositivo_socket]
            break

# Função principal do broker
def main():
    # Criação do socket do broker
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)

    print(f"Broker iniciado em {HOST}:{PORT}")

    while True:
        # Aceita novas conexões dos dispositivos
        dispositivo_socket, client_addr = server.accept()
        print(f"dispositivo conectado: {client_addr}")

        # Adiciona o dispositivo ao dicionário de dispositivos
        dispositivos[dispositivo_socket] = client_addr

        # Inicia uma thread para lidar com a conexão do dispositivo
        client_thread = threading.Thread(target=handle_client, args=(dispositivo_socket,))
        client_thread.start()
