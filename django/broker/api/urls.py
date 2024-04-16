from django.urls import path, include
from django.http import HttpResponse
from .views import my_view
from rest_framework.routers import DefaultRouter
from .views import MyAPIView

urlpatterns = [
    path('', my_view),
    path('api/', MyAPIView.as_view(), name='api'),
]


# O FRONT-END VAI FAZER UMA REQUEST PARA A API 
# NESSA REQUEST, ELE VAI MANDAR O TIPO DE SOLICITAÇÃO (TEMPERTURA, UMIDADE) (POST)
# O BROKER TRATA
# A API RESPONSE ENTREGA O RESULTADO DA TEMPERATURA/UMIDADE PARA O FRONT-END