from django.urls import path, include
from django.http import HttpResponse
from .views import my_view

urlpatterns = [
    path('', my_view)
]
