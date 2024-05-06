<div align="center">

# Internet of things (IOT)

</div>

# Resumo

<p align="justify">Este relatório aborda a implementação de um Broker utilizando o framework Django, um emulador de dispositivo e uma aplicação, com foco na interconexão desses elementos. O Broker recebe solicitações da aplicação (cliente) por meio de uma API REST e se comunica com os dispositivos através de uma conexão socket TCP. Os dados dos dispositivos são recebidos pelo Broker por meio de uma porta UDP e, em resposta às requisições do cliente, o Broker fornece uma resposta baseada nos dados adquiridos dos dispositivos. Este projeto foi desenvolvido como parte dos estudos da disciplina de Concorrência e Conectividade na Universidade Estadual de Feira de Santana (UEFS).</p>

# Arquitetura da solução (componentes e mensagens)

<p align="justify">A arquitetura da solução é composta por três principais componentes: o Broker, o emulador de dispositivo e a aplicação cliente.</p>

<p align="justify">Broker: O Broker é o componente central do sistema, responsável por receber requisições da aplicação cliente via API REST (porta 1026). Ele se comunica com os dispositivos por meio de uma conexão socket TCP (porta dinâmica), recebendo dados desses dispositivos através de uma porta UDP (1025). O Broker processa as requisições recebidas, interage com os dispositivos conforme necessário e envia respostas adequadas de volta para a aplicação cliente. Para o dispositivo se conectar pela primeira vez com o Broker, é inserido o IP do servidor Broker e a porta do dispositivo a ser conectado. Além disso, é usado a porta 1028 para realizar a primeira comunicação entre o dispositivo e o Broker. </p>

<p align="justify">O Broker utiliza o Framework Django, escrito em Python, para implementação da API REST. O arquivo broker/api/views.py é responsável por lidar com as requisições e o arquivo broker/api/scripts/connection_sensor.py por fazer as conexões com os dispositivos salvos no Banco de Dados.</p>

<p align="justify">O arquivo broker/api/models.py é uma parte arquitetural do Django que lida com o ORM, com a transcrição de objetos Python em registros no Banco de Dados. A classe Dispositivo é a entidade/tabela do Banco de Dados sqlite3.</p>

<p align="justify">O arquivo broker/initialize.py é o arquivo que inicia o Broker, abrindo duas threads: uma para rodar o servidor web Django e outra para escutar na porta 1028 a conexão de qualquer dispositivo. Quando recebe a conexão, o Broker registra no arquivo broker/api/buffer/cache.txt os dados desse dispositivo. Quando houver uma requisição GET, os dados em cache.txt são salvos no Banco de Dados.</p>

<p align="justify">Emulador de Dispositivo: Este componente simula o comportamento de dispositivos reais no sistema. Ele pode gerar dados de medição aleatórios e responder a comandos enviados pelo Broker. O emulador de dispositivo ajuda no desenvolvimento e teste do sistema, permitindo que diferentes cenários de interação entre dispositivos e o Broker sejam simulados de forma controlada.</p>

<p align="justify">Aplicação Cliente: A aplicação cliente é a interface através da qual os usuários interagem com o sistema. Ela envia requisições ao Broker por meio da API REST, solicitando informações, comandando ações nos dispositivos ou realizando outras operações específicas do sistema. A aplicação cliente recebe as respostas do Broker e apresenta essas informações de forma adequada ao usuário final.</p>

<p align="justify">As mensagens trocadas entre esses componentes incluem solicitações da aplicação cliente ao Broker, como pedidos de dados de dispositivos ou envio de comandos, mensagens de dados enviadas pelos dispositivos ao Broker, e respostas do Broker para a aplicação cliente, contendo informações solicitadas ou confirmações de ações realizadas. Essa comunicação é fundamental para o funcionamento integrado e eficiente do sistema como um todo.</p>

# Protocolo de comunicação entre dispositivo e Broker 

## Camada de aplicação

## Camada de transporte

# Interface da Aplicação (REST)

# Formatação, envio e tratamento de dados

# Tratamento de conexões simultâneas (threads)

# Gerenciamento do dispositivo

# Desempenho (uso de cache no Broker, filas, threads, etc.)

# Confiabilidade da solução (tratamento das conexões)

# Documentação do código

# Emprego do Docker

Siga os seguintes passos no terminal para executar o broker: 
- ```git clone https://github.com/douglasojesus/internet-of-things```
- ```cd internet-of-things/broker/```
- ```sudo docker build -t broker .```
- ```sudo docker run --network='host' -it --name container_broker broker```

Com isso, o servidor Broker já está rodando na porta 1026.

Para emular o dispositivo, abra outro terminal e navegue no diretório clonado:
- ```cd internet-of-things/sensor/```
- ```sudo docker build -t sensor .```
- ```sudo docker run --network='host' -it --name container_sensor sensor```

Para exibir a aplicação, abra outro terminal e navegue no diretório clonado:
- ```cd internet-of-things/aplicacao/```
- ```sudo docker build -t aplicacao .```
- ```sudo docker run --network='host' -it -u=$(id -u $USER):$(id -g $USER) -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix:rw -v --rm aplicacao```

Se quiser testar a API independente da aplicação, execute no terminal:
- ```curl http://localhost:8000/api/```
- ```curl -X POST http://localhost:8000/api/ -H "Content-Type: application/json" -d '{"id": 1, "comando": "dados"}'```

Método GET retorna todos dispositivos cadastrados.
Comandos disponíveis: ligar, desligar, dados.

