import socket
import random
import threading
import time

HOST = '0.0.0.0'
UDP_PORT_FIRST_CONNECTION = 1028
UDP_PORT = 1025  # Porta para comunicação UDP - porta do broker
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

def envia_porta_para_broker(SERVER_IP, TCP_PORT, NOME, MEDICAO, sock):
    while True:
        time.sleep(1)
        data = f"('{NOME}', '{MEDICAO}', {TCP_PORT}, '{MEU_IP}')"
        sock.sendto(data.encode(), (SERVER_IP, UDP_PORT_FIRST_CONNECTION))
        recebido = recebe_conexao(server)
        # Confirma recebimento
        if recebido[1] == "recebido":
            break

def generate_number():
    return round(random.uniform(20, 30), 2)  

def listen_to_socket(server, dados_dispositivo):
    while True:
        broker_info, dados = recebe_conexao(server)
        print(broker_info)
        value = "comando inválido"
        if dados == "dados":
            if dados_dispositivo["status"] == True:
                if dados_dispositivo["valor_aleatorio"] == True:
                    value = generate_number()
                else:
                    value = dados_dispositivo["medicao_atual"]
            else:
                value = "dispositivo desligado"
        elif dados == "ligar":
            dados_dispositivo["status"] = True
            value = "ligado"
        elif dados == "desligar":
            dados_dispositivo["status"] = False
            value = "desligado"

        solicita_conexao(value, sock, SERVER_IP)
        print("Para exibir o menu novamente, basta clicar em enter.")

        time.sleep(1)


def menu():
    return input("""
Informe o comando:
(1) Alterar medição atual;
(2) Ligar dispositivo;
(3) Desligar dispositivo;
(4) Acionar valores aleatórios;
>> 
""")

def permanece_conexao(nome, medicao, server):
    dados_dispositivo = {"tipo_medicao": medicao,
                         "nome": nome,
                         "medicao_atual": '',
                         "status": False,
                         "valor_aleatorio": True,
                         }
    while True:
        opcao = menu()
        if opcao == "1":
            dados_dispositivo["medicao_atual"] = input("Informe a medição atual >> ")
            dados_dispositivo["valor_aleatorio"] = False
        elif opcao == "2" and dados_dispositivo["status"] == False:
            dados_dispositivo["status"] = True
            listener_thread = threading.Thread(target=listen_to_socket, args=(server, dados_dispositivo))
            listener_thread.start()
        elif opcao == "3" and dados_dispositivo["status"] == True:
            dados_dispositivo["status"] = False
            listener_thread.join()
        elif opcao == "4":
            dados_dispositivo["valor_aleatorio"] = True
        else:
            print("Insira um comando (1, 2, 3 ou 4).")


if __name__ == '__main__':
    SERVER_IP = input("Qual o IP do servidor? >> ")
    TCP_PORT = int(input("Qual a porta desse dispositivo (01028-65535)? >> "))
    while TCP_PORT < 1028 or TCP_PORT > 65535 or TCP_PORT == 8000:
        TCP_PORT = int(input("A porta precisa estar entre 01028 e 65535. >> "))
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, TCP_PORT))
    server.listen(1) 
    # tentar colocar para fechar quando o usuário inserir off e abrir quando tiver em on

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    entrada = input("Dispositivo já foi instalado no broker? (S/N)\n>> ")
    if entrada.lower() == "n":
        NOME = input("Qual o nome deste dispositivo? >> ")
        MEDICAO = input("Que tipo de medição este dispositivo faz? >> ")
        envia_porta_para_broker(SERVER_IP, TCP_PORT, NOME, MEDICAO, sock)
    
    permanece_conexao(NOME, MEDICAO, server)

    server.close()
    
