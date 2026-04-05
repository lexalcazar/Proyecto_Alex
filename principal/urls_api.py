

# Creamos el router para las APIs
from django.urls import path, include
from rest_framework import routers

from principal.api_views import SalaViewSet, UsuarioViewSet, salas_por_ciudad

router = routers.DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'salas', SalaViewSet, basename='sala')

urlpatterns = [
    path('', include(router.urls)),
    path('salas/ciudad/<str:ciudad>/', salas_por_ciudad, name='salas-por-ciudad'),
   
]