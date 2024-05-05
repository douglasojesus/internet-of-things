import os
import threading
import time
import socket

HOST = '0.0.0.0' 
UDP_PORT = 44444

# Função para simular recebimento contínuo de dispositivos
def recebe_porta_do_dispositivo():
    while True:
        print("Aguardando conexão de dispositivo...")
        server_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_udp.bind((HOST, UDP_PORT)) # escutando na porta UDP_PORT
        data, addr = server_udp.recvfrom(1024)
        data = eval(data) # format: (nome, medicao, porta, ip)

        print(data)

        with open('api/buffer/cache.txt', 'a+') as arquivo:
            arquivo.write(f"('{data[0]}', '{data[1]}', {data[2]}, '{data[3]}')\n")

        print("Conexão guardada em cache.")

        server_udp.close()

        time.sleep(1)  # Simulação de espera por conexões

def iniciar_servidor_django():
	os.system("python3 manage.py makemigrations")
	os.system("python3 manage.py migrate")
	os.system("python3 manage.py runserver 0.0.0.0:8000")

def main():
    # Inicia uma thread para receber informações do dispositivo
    dispositivo_thread = threading.Thread(target=recebe_porta_do_dispositivo)
    dispositivo_thread.start()

    # Inicia o servidor Django em uma thread separada
    django_thread = threading.Thread(target=iniciar_servidor_django)
    django_thread.start()

    # Aguarda as threads terminarem (isso mantém o programa principal rodando)
    dispositivo_thread.join()
    django_thread.join()

if __name__ == '__main__':
    main()
