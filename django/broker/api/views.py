from django.shortcuts import render
from .scripts.conection_sensor import solicita_conexao, recebe_conexao, main
from rest_framework import viewsets
from .models import DataConnection
from .serializers import DataConnectionSerializer

class DataConnectionViewSet(viewsets.ModelViewSet):
    queryset = DataConnection.objects.all()
    serializer_class = DataConnectionSerializer

def my_view(request):
    return render(request, "index.html")

# o back-end recebe o comando + um identificador da aplicação que efetua a requisição


