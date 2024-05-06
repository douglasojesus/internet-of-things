import socket
import time
import threading

HOST = '0.0.0.0' 
UDP_PORT = 1025  # Porta para comunicação UDP - porta do broker

""" Função que retorna o IP do servidor. """
def ver_ip():
    return socket.gethostbyname(socket.gethostname())

""" Função que retorna os dados obtidos do dispositivo via conexão UDP. """
def recebe_conexao():
    global UDP_PORT
    server_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_udp.bind((HOST, UDP_PORT))
    print(f"Servidor UDP aguardando conexões em {UDP_PORT}")
    data, addr = server_udp.recvfrom(1024)
    print(f"Dados recebidos via UDP de {addr}: {data.decode()}")
    server_udp.close()
    return addr, data

""" Função que se comunica com o dispositivo via TCP. """
def solicita_conexao(dispositivo, comando):
    try:
        data = f"{comando}"
        sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_tcp.connect((dispositivo.ip, dispositivo.porta))
        sock_tcp.sendall(data.encode())
        print(f"Dados enviados via TCP: {data}")
        sock_tcp.close()
        return True
    except Exception as e:
        print(f"Erro ao enviar dados via TCP: {e}")
        time.sleep(2)
        return False
    
""" Função que se conecta com o dispositivo adicionado e retorna as informações do dispositivo. """
def recebe_porta_do_dispositivo():
    server_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_udp.bind((HOST, UDP_PORT))
    data, addr = server_udp.recvfrom(1024)
    is_recebido = "recebido"
    data = eval(data)
    sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_tcp.connect((data[2], data[1]))
    sock_tcp.sendall(is_recebido.encode())
    server_udp.close()
    return data # formato: (id, porta, IP)
