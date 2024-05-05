import socket
import random
import threading
import time

HOST = '0.0.0.0'
UDP_PORT = 1025  # Porta para comunicação UDP - porta do broker
SENSOR_ID = 'sensor1'  # Identificador do sensor
MEU_IP = socket.gethostbyname(socket.gethostname())

def recebe_conexao(server): 
    conexao, client_addr = server.accept()
    data = conexao.recv(1024).decode()
    print(f"Dispositivo conectado: {client_addr}") 
    print(f'Dados recebidos: {data}')
    conexao.close()
    return client_addr, data

def solicita_conexao(data, sock, SERVER_IP):
    data = f"{data}"
    sock.sendto(data.encode(), (SERVER_IP, UDP_PORT))
    print(f"Dados enviados: {data}")

def envia_porta_para_broker(SERVER_IP, TCP_PORT, NOME, MEDICAO):
    time.sleep(1)
    data = f"('{NOME}', '{MEDICAO}', {TCP_PORT}, '{MEU_IP}')" 
    sock.sendto(data.encode(), (SERVER_IP, UDP_PORT))
    print(SERVER_IP, UDP_PORT, "enviado para broker")

def generate_number():
    return round(random.uniform(20, 30), 2)  

def listen_to_socket(server):
    while True:
        print("Dispositivo Startado")
        broker_info = recebe_conexao(server)
        print(broker_info)
        value = generate_number()
        solicita_conexao(value, sock, SERVER_IP)
        time.sleep(1)

def habilita_desabilita_conexao():
    anterior = ''
    while True:
        time.sleep(1)
        comando = input("Digite 'conectar' para escutar na porta ou 'desconectar' para parar de escutar: ")
        if comando != anterior:
            anterior = comando
            if comando.lower() == "conectar":
                listener_thread = threading.Thread(target=listen_to_socket, args=(server,))
                listener_thread.start()
            elif comando.lower() == "desconectar":
                listener_thread.join()
                print("Desconectado. Para o broker se conectar novamente, digite conectar.")
            else:
                print("Comando inválido.")


if __name__ == '__main__':
    SERVER_IP = input("Qual o IP do servidor? >> ")
    TCP_PORT = int(input("Qual a porta desse dispositivo (01028-65535)? >> "))
    while TCP_PORT < 1028 or TCP_PORT > 65535 or TCP_PORT == 8000:
        TCP_PORT = int(input("A porta precisa estar entre 01028 e 65535. >> "))
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, TCP_PORT))
    server.listen(1) 
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    entrada = input("Dispositivo já foi instalado no broker? (S/N)\n>> ")
    if entrada.lower() == "n":
        NOME = input("Qual o nome deste dispositivo? >> ")
        MEDICAO = input("Que tipo de medição este dispositivo faz? >> ")
        envia_porta_para_broker(SERVER_IP, TCP_PORT, NOME, MEDICAO)
    
    thread_habilita = threading.Thread(target=habilita_desabilita_conexao)
    thread_habilita.start()
    
