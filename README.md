# internet-of-things

Siga os seguintes passos no terminal para executar o broker: 
- git clone https://github.com/douglasojesus/internet-of-things
- cd internet-of-things/broker/
- sudo docker build -t broker .
- sudo docker run --network='host' -it --name container server

Com isso, o servidor Broker já está rodando na porta 1026.

Para emular o dispositivo, abra outro terminal e navegue no diretório clonado:
- python3 internet-of-things/sensor/dispositivo.py

Para exibir a aplicação, abra outro terminal e navegue no diretório clonado:
- python3 internet-of-things/aplicacao/main.py

Se quiser testar a API independente da aplicação, execute no terminal:
- curl http://localhost:8000/api/
- curl -X POST http://localhost:8000/api/ -H "Content-Type: application/json" -d '{"id": 1, "comando": "dados"}'

Método GET retorna todos dispositivos cadastrados.
Comandos disponíveis: ligar, desligar, dados.

