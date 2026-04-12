from datetime import datetime
from rest_framework import viewsets
from rest_framework.response import Response
from principal.models import Grupo, Sala, Usuario, DisponibilidadSala
from principal.api.seriallizers import CreateGrupoSerializer, CreateSalaSerializer, CreateSalaSerializer, CreateUsuarioSerializer, GrupoSerializer, SalaSerializer, SalaSerializer, UsuarioSerializer, CreateDisponibilidadSalaSerializer, DisponibilidadSalaSerializer
from rest_framework.decorators import api_view

from rest_framework import status
# Vistas usuarios
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    def get_serializer_class(self):
        """Usa diferente serializer según la acción"""
        if self.action in ['create', 'update', 'partial_update']:
            return CreateUsuarioSerializer
        return UsuarioSerializer

# Vistas salas
class SalaViewSet(viewsets.ModelViewSet):
    queryset = Sala.objects.all()
    def get_serializer_class(self):
        """Usa diferente serializer según la acción"""
        if self.action in ['create', 'update', 'partial_update']:
            return CreateSalaSerializer
        return SalaSerializer

# Vistas grupos
class GrupoViewSet(viewsets.ModelViewSet):
    queryset = Grupo.objects.all()
    def get_serializer_class(self):
        """Usa diferente serializer según la acción"""
        if self.action in ['create', 'update', 'partial_update']:
            return CreateGrupoSerializer
        return GrupoSerializer
    def get_queryset(self):
        queryset = super().get_queryset()

        nombre = self.request.query_params.get('nombre')

        if nombre:
            queryset = queryset.filter(nombre__icontains=nombre)

        return queryset

# Vista disponibilidad salas
class DisponibilidadSalaViewSet(viewsets.ModelViewSet):
    queryset = DisponibilidadSala.objects.all()
    def get_serializer_class(self):
        """Usa diferente serializer según la acción"""
        if self.action in ['create', 'update', 'partial_update']:
            return CreateDisponibilidadSalaSerializer
        return DisponibilidadSalaSerializer

# patrones personalizados

@api_view(['GET'])
def salas_por_ciudad(request, ciudad):
    """Devuelve las salas filtradas por ciudad"""
    salas = Sala.objects.filter(ciudad=ciudad)
    serializer = SalaSerializer(salas, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def grupos_por_ciudad(request, ciudad):
    """Devuelve los grupos filtrados por ciudad"""
    grupos = Grupo.objects.filter(ciudad=ciudad)
    serializer = GrupoSerializer(grupos, many=True)
    return Response(serializer.data)
@api_view(['GET'])
def disponibilidad_salas_por_fecha(request, fecha):
    """Devuelve la disponibilidad de las salas filtrada por fecha"""

    try:
        fecha_convertida = datetime.strptime(fecha, "%Y-%m-%d").date()
    except ValueError:
        return Response(
            {"error": "Formato de fecha inválido. Usa YYYY-MM-DD"},
            status=status.HTTP_400_BAD_REQUEST
        )

    disponibilidad = DisponibilidadSala.objects.filter(
        fecha=fecha_convertida,
        estado='disponible'
    )

    serializer = DisponibilidadSalaSerializer(disponibilidad, many=True)
    return Response(serializer.data)
# ENDPOINT BUSCAR GRUPO POR NOMBRE
