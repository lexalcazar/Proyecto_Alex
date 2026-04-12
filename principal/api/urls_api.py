

# Creamos el router para las APIs
from django.urls import path, include
from rest_framework import routers

from principal.api.api_views import DisponibilidadSalaViewSet, GrupoViewSet, SalaViewSet, UsuarioViewSet, disponibilidad_salas_por_fecha, grupos_por_ciudad, salas_por_ciudad

router = routers.DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'salas', SalaViewSet, basename='sala')
router.register(r'grupos', GrupoViewSet, basename='grupo')
router.register(r'disponibilidad-salas', DisponibilidadSalaViewSet, basename='disponibilidad-sala')

urlpatterns = [
    path('', include(router.urls)),
    path('salas/ciudad/<str:ciudad>/', salas_por_ciudad, name='salas-por-ciudad'),
    path('grupos/ciudad/<str:ciudad>/', grupos_por_ciudad, name='grupos-por-ciudad'),
    path(
        'disponibilidad-salas/fecha/<str:fecha>/',
        disponibilidad_salas_por_fecha,
        name='disponibilidad-salas-por-fecha'
    ),
    

]