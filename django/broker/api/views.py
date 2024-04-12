from django.shortcuts import render
import socket

def my_view(request):
    return render(request, "index.html")


