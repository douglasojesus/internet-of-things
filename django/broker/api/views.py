from django.shortcuts import render
from .scripts.conection_sensor import solicita_conexao, recebe_conexao, recebe_porta_do_dispositivo


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
        dados = request.data 
        try:
            if dados.get('comando') == 'adicionar_dispositivo':
                novo_dispositivo = recebe_porta_do_dispositivo()
                if Dispositivo.objects.filter(porta=novo_dispositivo[1]).first():
                    return Response({'value': 'já existe um dispositivo salvo com essa porta. configure uma nova porta para o dispositivo.'})
                dispositivo = Dispositivo()
                dispositivo.tipo_medicao = dados.get('tipo_medicao')
                dispositivo.porta = novo_dispositivo[1]
                dispositivo.nome = novo_dispositivo[0]
                dispositivo.ip = novo_dispositivo[2]
                dispositivo.save()
                return Response({'value': 'dispositivo salvo'})
            else:
                dispositivo_id = dados.get('id')
                dispositivo = Dispositivo.objects.get(pk=dispositivo_id)
                if dados.get('comando') == "ligar":
                    dispositivo.esta_ativo = True
                    dispositivo.save()
                    return Response({'value': 'ligado'}, status=status.HTTP_201_CREATED)
                elif dados.get('comando') == 'desligar':
                    dispositivo.esta_ativo = False
                    dispositivo.save()
                    return Response({'value': 'desligado'}, status=status.HTTP_201_CREATED)
                elif dados.get('comando') == 'dados':
                    if dispositivo.esta_ativo:
                        if solicita_conexao(dispositivo, dispositivo.tipo_medicao):
                            addr, data = recebe_conexao()
                        print(data)
                        dispositivo.medicao_atual = data
                        dispositivo.save()
                        return Response({'value': dispositivo.medicao_atual}, status=status.HTTP_201_CREATED)
                    else:
                        return Response({'error': 'Dispositivo nao esta ligado.'})              
                else:
                    return Response({'error': 'Dispositivo so aceita os comandos: ligar, desligar, dados.', 'formato': '{"id": numero, "comando": "comando"}'})
        except Dispositivo.DoesNotExist:
            return Response({'error': 'Dispositivo nao encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        except UnboundLocalError:
            return Response({'error': 'Dispositivo pode estar fora da tomada.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        #except Exception as e:
        #    return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def my_view(request):
    return render(request, "index.html")

# o back-end recebe o comando + um identificador da aplicação que efetua a requisição


