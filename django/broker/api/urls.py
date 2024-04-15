from django.urls import path, include
from django.http import HttpResponse
from .views import my_view
from rest_framework.routers import DefaultRouter
from .views import DataConnectionViewSet

router = DefaultRouter()
router.register('', DataConnectionViewSet)


urlpatterns = [
    path('', my_view),
    path('api/', include(router.urls)),
]
