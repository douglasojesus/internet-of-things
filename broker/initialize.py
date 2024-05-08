import os
import threading
import time
import socket
import queue

HOST = '0.0.0.0' 
UDP_PORT_FIRST_CONNECTION = 1028

# Fila para escrita no arquivo cache.txt
fila_cache = queue.Queue()

# Função para consumir a fila de conexões primárias e escrever no arquivo cache.txt
def escrever_cache():
    while True:
        data = fila_cache.get()
        with open('api/buffer/cache.txt', 'a+') as arquivo:
            arquivo.write(f"{data}\n")
        fila_cache.task_done()

     
# Função para receber dados do dispositivo e adicionar na fila de escrita
def recebe_porta_do_dispositivo():
    while True:
        # Recebe conexão do dispositivo
        server_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_udp.bind((HOST, UDP_PORT_FIRST_CONNECTION))
        data, addr = server_udp.recvfrom(1024)
        data = eval(data)
        server_udp.close()

        # Retorna informando que foi recebido com sucesso.
        sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Received data: ", data)
        sock_tcp.connect((data[3], data[2])) # (ip, porta)
        sock_tcp.sendall("{'name': '', 'command': 'received'}".encode())
        server_udp.close()

        fila_cache.put(f"('{data[0]}', '{data[1]}', {data[2]}, '{data[3]}')")

        time.sleep(1)

# Função que realiza as migrações e roda o servidor Django
def iniciar_servidor_django():
	os.system("python3 manage.py makemigrations")
	os.system("python3 manage.py migrate")
	os.system("python3 manage.py runserver 0.0.0.0:1026")

def main():
    # Inicia uma thread para receber informações do dispositivo
    dispositivo_thread = threading.Thread(target=recebe_porta_do_dispositivo)
    dispositivo_thread.start()

    # Inicia a thread para escrever no arquivo cache.txt
    thread_escrita = threading.Thread(target=escrever_cache)
    thread_escrita.start()

    # Inicia o servidor Django em uma thread separada
    django_thread = threading.Thread(target=iniciar_servidor_django)
    django_thread.start()

    # Aguarda as threads terminarem (isso mantém o programa principal rodando)
    dispositivo_thread.join()
    thread_escrita.join()
    django_thread.join()

if __name__ == '__main__':
    main()
