from django.shortcuts import render
from .scripts.conection_sensor import solicita_conexao, recebe_conexao, main


from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Dispositivo
from django.core.serializers import serialize

class MyAPIView(APIView):
    def get(self, request):
        dispositivos = Dispositivo.objects.all()
        # Serializa os objetos Dispositivo em JSON
        dispositivos_json = serialize('json', dispositivos)
        return Response(dispositivos_json)

    def post(self, request):
        # verifica o tipo de solicitação. se é temperatura, etc.
        # Acessando os dados enviados pelo usuário no corpo da requisição
        dados = request.data # formato: {"valor": "Temperatura"} -> {"id": }
        try:
            dispositivo_id = dados.get('id')
            dispositivo = Dispositivo.objects.get(pk=dispositivo_id)
            if solicita_conexao(dispositivo.tipo_medicao):
                addr, data = recebe_conexao()
            dispositivo.medicao_atual = data
            return Response({'value': dispositivo.medicao_atual})
        except Dispositivo.DoesNotExist:
            return Response({'error': 'Dispositivo não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        # retorna o dado solicitado
        resultado = dados #valor pego do connection_sensor
        
        return Response({'message': 'Dados recebidos com sucesso!', 'valor': resultado}, status=status.HTTP_201_CREATED)

def my_view(request):
    return render(request, "index.html")

# o back-end recebe o comando + um identificador da aplicação que efetua a requisição


