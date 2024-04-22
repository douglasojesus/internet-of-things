import socket
import threading

# Configurações do broker
HOST = '0.0.0.0'  # Escuta em todas as interfaces
PORT = 9999  # Porta do broker

# Dicionário para armazenar as conexões dos dispositivos
dispositivos = {}

# Função para lidar com as conexões dos dispositivos
def handle_client(dispositivo_socket, client_addr):
    while True:
        try:
            # Recebe dados do dispositivo via UDP
            data, addr = dispositivo_socket.recvfrom(1024)
            if not data:
                print(f"Dispositivo desconectado: {client_addr}")
                del dispositivos[client_addr]
                break

            # Encaminha a mensagem para todos os dispositivos conectados (exceto o remetente)
            for client in dispositivos:
                if client != client_addr:
                    client.sendto(data, client)

        except:
            print(f"Erro ao lidar com dispositivo: {client_addr}")
            del dispositivos[client_addr]
            break

# Função principal do broker
def main():
    # Criação do socket do broker (UDP)
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((HOST, PORT))

    print(f"Broker UDP iniciado em {HOST}:{PORT}")

    while True:
        # Recebe dados do dispositivo via UDP
        data, addr = server.recvfrom(1024)
        print(f"Dados recebidos do dispositivo {addr}: {data.decode()}")

        # Adiciona o dispositivo ao dicionário de dispositivos
        dispositivos[addr] = addr

        # Inicia uma thread para lidar com a conexão do dispositivo
        client_thread = threading.Thread(target=handle_client, args=(server, addr))
        client_thread.start()

if __name__ == "__main__":
    main()

"""
No UDP, não há um estado de conexão persistente como no TCP, onde o servidor "escuta" e aceita conexões de clientes. Em UDP, cada pacote é tratado independentemente, e o servidor não mantém uma conexão contínua com os clientes.

Concorrência de Pacotes: Como UDP é um protocolo não orientado a conexão e não garante a entrega ordenada ou confiável dos pacotes, os pacotes enviados por vários dispositivos podem chegar ao broker de forma concorrente e em ordens diferentes da enviada pelos dispositivos.

Perda de Pacotes: Como não há garantia de entrega, pode ocorrer a perda de pacotes durante a transmissão, especialmente se a rede estiver congestionada ou houver problemas de latência.

Processamento Paralelo: O broker deve ser capaz de lidar com a chegada simultânea de pacotes de vários dispositivos e processá-los de forma paralela. Isso pode exigir a implementação de lógica de concorrência ou uso de threads para lidar com múltiplos pacotes ao mesmo tempo.

Ordenação e Identificação: O broker deve ser capaz de identificar a origem de cada pacote recebido para garantir que as informações sejam tratadas corretamente e associadas aos dispositivos corretos.

Tratamento de Erros: Como UDP não detecta erros de transmissão, o broker deve implementar mecanismos para lidar com possíveis erros, como reenvio de pacotes ou confirmações de recebimento, se necessário.

"""