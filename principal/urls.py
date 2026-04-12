from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('fechas-disponibles/<int:sala_id>/', views.fechas_disponibles_view, name='fechas_disponibles'),
    path('listado-salas/', views.listado_salas, name='listado_salas'),
    path('listado-grupos/', views.listado_grupos, name='listado_grupos'),
    path('cuenta-publica-grupos/<int:id>/', views.cuenta_publica_grupos, name='cuenta_publica_grupos'),
    path('cuenta-publica-salas/<int:id>/', views.cuenta_publica_salas, name='cuenta_publica_salas'),
    path('buscar/', views.buscar, name='buscar'),
    path('buscador/', views.buscador, name='buscador'),
]