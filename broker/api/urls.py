from django.urls import path
from django.http import HttpResponse
from .views import my_view
from .views import MyAPIView

# Roteamento do servidor web
urlpatterns = [
    path('', my_view),
    path('api/', MyAPIView.as_view(), name="my-api-view"),
]
