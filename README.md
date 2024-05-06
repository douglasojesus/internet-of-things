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

<p align="center">
  <img src="docs/imgs/Arquitetura.png" alt="Figura 1.">
</p>

<p align="justify">As mensagens trocadas entre esses componentes incluem solicitações da aplicação cliente ao Broker, como pedidos de dados de dispositivos ou envio de comandos, mensagens de dados enviadas pelos dispositivos ao Broker, e respostas do Broker para a aplicação cliente, contendo informações solicitadas ou confirmações de ações realizadas. Essa comunicação é fundamental para o funcionamento integrado e eficiente do sistema como um todo.</p>

# Protocolo de comunicação entre dispositivo e Broker 

## Camada de aplicação

<p align="justify">Na camada de aplicação, que atua como a interface para interações entre sistemas via rede, utiliza-se o modelo cliente-servidor para a comunicação eficiente entre o broker e os dispositivos.</p>

<p align="justify">Nesse modelo, o Broker assume o papel de servidor, fornecendo informações para aplicações (servidor HTTP) e dispositivos (servidor UDP). Ele permanece sempre ativo, recebendo solicitações iniciais dos dispositivos e gerenciando as requisições feitas pela interface do usuário, além de encaminhar essas solicitações aos dispositivos e retornar suas respostas. Do lado do dispositivo, ele também é um servidor, mas do tipo TCP, para escutar na porta dinâmica (registrada no momento de ligação do dispositivo) comandos recebidos do Broker.</p>

<p align="justify">Inicialmente, o Dispositivo inicia uma comunicação UDP para estabelecer uma conexão com o Broker, enviando um nome, tipo de medição, porta e seu IP, que serão utilizados posteriormente. Após esse processo, o Dispositivo fica disponível para receber comandos do Broker, como o envio de dados.</p>

<p align="justify">Do outro lado, o Broker recebe a primeira comunicação do dispositivo e registra os dados em uma cache. Quando é feito uma requisição através da API REST, os dados são removidos da cache e salvos no Banco de Dados. Essa foi uma escolha para melhorar o desempenho do servidor. Após salvo o dispositivo, o Broker enviará requisições TCP para o dispositivo com a porta e IP adicionados anteriormente. Essas requisições estarão de acordo com as requisições feitas pelo usuário através da API REST.</p>

## Camada de transporte

<p align="justify">Na camada de transporte, a integração entre os dispositivos e o Broker foi realizada por meio de protocolos específicos, como solicitados no problema inicial. A seguir, descrevo detalhadamente a dinâmica dessa interação entre os dispositivos e o Broker:</p>

### Protocolos de Comunicação:

<p align="justify">O Broker utiliza o protocolo UDP (User Datagram Protocol) para receber dados dos dispositivos, operando em uma porta dedicada (porta 1025). Essa escolha foi feita devido a descrição da atividade proposta e às suas características que resultam em menor sobrecarga, devido a falta de controle de fluxo e retransmissão, o que gera menor tempo de resposta. Os dispositivos emulados transmitem os dados para o Broker por meio dessa porta UDP.</p>

<p align="justify">Quando o Broker necessita estabelecer contato com um dispositivo específico, ele inicia uma conexão TCP (Transmission Control Protocol) com o dispositivo correspondente. Por meio dessa conexão TCP, o Broker envia comandos ou requisita dados ao dispositivo, visto a necessidade de uma abordagem confiável para os comandos de gerenciamento. Ele alcança essa abordagem confiável por meio de técnicas como confirmações de recebimento e retransmissão de dados perdidos, o que garante que comandos e solicitações não sejam perdidos. </p>

# Interface da Aplicação (REST)

<p align="justify">A interface da aplicação baseada em REST é implementada por meio de um código que utiliza a biblioteca tkinter para a criação de uma interface gráfica de usuário (GUI). Esta GUI permite interações com os serviços de rede do sistema, facilitando a comunicação entre o usuário e os dispositivos controlados pelo broker. Quanto às requisições, a interface usa a biblioteca requests para efetuar requisições para a API.</p>

<p align="justify">O código da aplicação define uma classe Application, que herda as funcionalidades da classe tk.Tk do tkinter. Nesta classe, são criados elementos visuais como rótulos, menus, campos de entrada e botões para interação do usuário. Através desses elementos, o usuário pode realizar diversas operações relacionadas aos dispositivos controlados pelo broker.</p>

## Verbos e Rotas na Camada de Aplicação

### 1. Ver dispositivos disponíveis
<p align="justify">Ao selecionar esta opção, a aplicação faz uma requisição GET para a API do broker, obtendo uma lista de dispositivos disponíveis. Essa lista é exibida na interface gráfica para o usuário. Quando essa requisição é feita, os dispositivos salvos em cache são adicionados no Banco de Dados.</p>
- **Verbo**: GET
- **Rota**: `http://localhost:1026/api/`

### 2. Ligar sensor
<p align="justify">Permite ao usuário enviar um comando para ligar um sensor específico. A aplicação envia uma requisição POST para a API do broker com o ID do dispositivo e o comando "ligar".</p>
- **Verbo**: POST
- **Rota**: `http://localhost:1026/api/`
- **Parâmetros**: `{"id": device_id, "comando": "ligar"}`

### 3. Desligar sensor
<p align="justify">Similar ao item anterior, porém envia o comando "desligar".</p>
- **Verbo**: POST
- **Rota**: `http://localhost:1026/api/`
- **Parâmetros**: `{"id": device_id, "comando": "desligar"}`

### 4. Solicitar medição atual do sensor
<p align="justify">Esta opção permite ao usuário solicitar a medição atual de um sensor específico. A aplicação envia uma requisição POST para a API do broker com o ID do dispositivo e o comando "dados". </p>
- **Verbo**: POST
- **Rota**: `http://localhost:1026/api/`
- **Parâmetros**: `{"id": device_id, "comando": "dados"}`

### 5. Ver IP do servidor (broker)
<p align="justify">Ao selecionar esta opção, a aplicação envia uma requisição POST para a API do broker com o comando "ver_ip_server", obtendo assim o IP do servidor. </p>
- **Verbo**: POST
- **Rota**: `http://localhost:1026/api/`
- **Parâmetros**: `{"comando": "ver_ip_server"}`

<p align="justify">Estas são as operações que a camada de aplicação executa na interação com a API do broker, utilizando os verbos HTTP e as rotas correspondentes para realizar as ações desejadas, como consultar dispositivos disponíveis, controlar sensores e obter informações do servidor (broker).</p>

<p align="justify">A  aplicação também trata possíveis erros de conexão ou respostas inválidas da API, exibindo mensagens de erro na interface gráfica para informar o usuário sobre o problema ocorrido.</p>


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

