# internet-of-things

No ambiente virtual, instale as dependências: 
- pip install -r requirements.txt

Navegue para o dispositivo e o execute:
- python3 internet-of-things/sensor/dispositivo.py

Em outra aba do terminal, rode o servidor django:
- python3 internet-of-things/django/broker/manage.py runserver

Em outra aba do terminal, teste a API:
- curl http://localhost:8000/api/
- curl -X POST http://localhost:8000/api/ -H "Content-Type: application/json" -d '{"id": 1, "comando": "dados"}'

Comandos disponíveis: ligar, desligar, dados.
