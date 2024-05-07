# Importa a função render do Django para renderização de templates
from django.shortcuts import render  
# Importa funções personalizadas relacionadas à conexão com sensores
from .scripts.conection_sensor import solicita_conexao, recebe_conexao, ver_ip  

# Importa o status HTTP do Django REST Framework
from rest_framework import status  
# Importa a classe APIView do Django REST Framework
from rest_framework.views import APIView  
# Importa a classe Response do Django REST Framework
from rest_framework.response import Response  
# Importa o modelo Dispositivo do Django
from .models import Dispositivo  
# Importa a função serialize do Django para serialização de objetos
from django.core.serializers import serialize  

# Classe de visualização para manipulação de dados através da API
class MyAPIView(APIView):
    # Método para lidar com solicitações GET
    def get(self, request):
        # Acessa o arquivo cache.txt e coleta todos os dispositivos salvos no arquivo e depois limpa o arquivo
        with open('api/buffer/cache.txt', 'r+') as arquivo:
            lista = []
            for linha in arquivo:
                lista.append(linha)
            arquivo.seek(0) 
            arquivo.truncate(0)
        # Se houve dispositivos em cache.txt, é percorrido entre todos esses dispositivos e salva sua correspondência no banco de dados
        if len(lista) > 0:
            for dados in lista:
                dados = eval(dados) # format: (nome, medicao, porta, ip)
                if Dispositivo.objects.filter(porta=dados[2]).first():
                    return Response({'value': 'já existe um dispositivo salvo com essa porta: ' + dados[2] + '. configure uma nova porta para o dispositivo.'})
                dispositivo = Dispositivo()
                dispositivo.nome = dados[0]
                dispositivo.tipo_medicao = dados[1] 
                dispositivo.porta = dados[2]
                dispositivo.ip = dados[3]
                dispositivo.esta_ativo = False
                dispositivo.save()
        dispositivos = Dispositivo.objects.all()
        # Serializa os objetos Dispositivo em JSON
        dispositivos_json = serialize('json', dispositivos)
        return Response(dispositivos_json)

    # Método para lidar com solicitações GET
    def post(self, request):
        # Acessando os dados enviados pelo usuário no corpo da requisição
        dados = request.data 
        try:
            if dados.get('comando') == 'ver_ip_server':
                return Response({'value': ver_ip()})
            else:
                dispositivo_id = dados.get('id')
                dispositivo = Dispositivo.objects.get(pk=dispositivo_id)
                try:
                    if dados.get('comando') == "ligar":
                        if solicita_conexao(dispositivo, "ligar"):
                            addr, valor = recebe_conexao()
                        dispositivo.esta_ativo = True
                        dispositivo.save()
                        return Response({'value': valor}, status=status.HTTP_201_CREATED)
                    elif dados.get('comando') == 'desligar':
                        if solicita_conexao(dispositivo, "desligar"):
                            addr, valor = recebe_conexao()
                        dispositivo.esta_ativo = False
                        dispositivo.save()
                        return Response({'value': valor}, status=status.HTTP_201_CREATED)
                    elif dados.get('comando') == 'dados':
                        if dispositivo.esta_ativo:
                            if solicita_conexao(dispositivo, "dados"):
                                addr, valor = recebe_conexao()
                            if (valor != 'off'):
                                dispositivo.medicao_atual = valor
                            else:
                                dispositivo.esta_ativo = False
                            dispositivo.save()
                            return Response({'value': valor}, status=status.HTTP_201_CREATED)     
                        else:
                            return Response({'error': 'Dispositivo esta desligado.'})      
                    else:
                        return Response({'error': 'Dispositivo so aceita os comandos: ligar, desligar, dados.', 'formato': '{"id": numero, "comando": "comando"}'})
                except UnboundLocalError:
                    dispositivo.esta_ativo = False
                    dispositivo.save()
                    return Response({'error': 'Dispositivo pode estar fora da tomada.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Dispositivo.DoesNotExist:
            return Response({'error': 'Dispositivo nao encontrado.'}, status=status.HTTP_404_NOT_FOUND)  
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def my_view(request):
    return render(request, "index.html")

