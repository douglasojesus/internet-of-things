import socket
import random
import time
import threading

HOST = '0.0.0.0'
DISPOSITIVO_IP = '127.0.0.1'  # IP do servidor 
TCP_PORT = 12345  # Porta para comunicação TCP
UDP_PORT = 54321  # Porta para comunicação UDP

def recebe_conexao(): # ELE TEM QUE SEMPRE RECEBER -> PRECISA INICIAR O RECEBE CONEXÃO ANTES DO DISPOSITIVO.
    global UDP_PORT
    server_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_udp.bind((HOST, UDP_PORT))
    print(f"Servidor UDP aguardando conexões em {UDP_PORT}")

    data, addr = server_udp.recvfrom(1024)
    print(f"Dados recebidos via UDP de {addr}: {data.decode()}")
    server_udp.close()
    return addr, data

def solicita_conexao(id_aplicacao, comando):
    global DISPOSITIVO_IP, TCP_PORT
    try:
        sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_tcp.connect((DISPOSITIVO_IP, TCP_PORT))
        data = f"{id_aplicacao} - {comando}"
        sock_tcp.sendall(data.encode())
        print(f"Dados enviados via TCP: {data}")
        sock_tcp.close()
    except Exception as e:
        print(f"Erro ao enviar dados via TCP: {e}")
        time.sleep(5)

def main():
    threads = []
    while True:
        # Inicia uma thread para lidar com a conexão do dispositivo
        recebe_dados_udp = threading.Thread(target=recebe_conexao, args=())
        threads.append(recebe_dados_udp)
        recebe_dados_udp.start()

        if thread in threads:
            for thread in threads:
                recebe_dados_udp.join()  # Aguarda a conclusão da thread
                resultado = recebe_dados_udp.resultado
                threads.remove(thread)
                # manipula resultado para retornar para aplicação correta

# FLUXO:
# ATIVA SERVIDOR UDP -> RECEBE REQUISIÇÃO -> SOLICITA CONEXÃO -> RECEBE CONEXÃO -> RESPONDE REQUISIÇÃO 

if __name__ == '__main__':
    while True:
        print("Broker Startado")
        input("Para enviar a solicitação, clique em enter.")
        solicita_conexao('teste', 'temperatura_atual')
        sensor_infos = recebe_conexao()
        time.sleep(5)
        # daqui devolve como response da API