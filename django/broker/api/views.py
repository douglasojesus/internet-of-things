from django.shortcuts import render
import socket

def my_view(request):
    return render(request, "index.html")

# o back-end recebe o comando + um identificador da aplicação que efetua a requisição


