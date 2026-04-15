from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from principal.models import Grupo, Sala, Usuario, DisponibilidadSala, Reserva
from principal.api.seriallizers import ConfirmacionReservaSerializer,ConfirmarReservaSerializer,CreateGrupoSerializer, CreateSalaSerializer, CreateSalaSerializer, CreateUsuarioSerializer, GrupoSerializer, SalaSerializer, SalaSerializer, UsuarioSerializer, CreateDisponibilidadSalaSerializer, DisponibilidadSalaSerializer, CreateReservaSerializer, ReservaSerializer
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework import status

from rest_framework.decorators import action
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
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CreateGrupoSerializer
        return GrupoSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        nombre = self.request.query_params.get('nombre')

        if nombre:
            queryset = queryset.filter(nombre__icontains=nombre)

        return queryset

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

# Vista disponibilidad salas
class DisponibilidadSalaViewSet(viewsets.ModelViewSet):
    queryset = DisponibilidadSala.objects.all()
    def get_serializer_class(self):
        """Usa diferente serializer según la acción"""
        if self.action in ['create', 'update', 'partial_update'] and self.request.user.rol == 'sala':
            return CreateDisponibilidadSalaSerializer
        return DisponibilidadSalaSerializer
    
# Vista para reservas
class EsGrupo(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol == 'grupo'

class EsSala(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol == 'sala'


class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()

    def get_queryset(self):
        user = self.request.user

        if user.rol == 'grupo':
            return Reserva.objects.filter(grupo__usuario=user)

        if user.rol == 'sala':
            return Reserva.objects.filter(sala__usuario=user)

        return Reserva.objects.none()

    def get_permissions(self):
        if self.action == 'create':
            return [EsGrupo()]
        if self.action == 'confirmar':
            return [EsSala()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateReservaSerializer
        if self.action == 'confirmar':
            return ConfirmarReservaSerializer
        return ReservaSerializer

    def update(self, request, *args, **kwargs):
        return Response({"error": "No permitido."}, status=405)

    def partial_update(self, request, *args, **kwargs):
        return Response({"error": "No permitido."}, status=405)

    @action(detail=True, methods=['put'], url_path='confirmar')
    def confirmar(self, request, pk=None):
        reserva = self.get_object()

        if request.user != reserva.sala.usuario:
            return Response(
                {"error": "No tienes permiso para confirmar esta reserva."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(reserva, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(ConfirmacionReservaSerializer(reserva).data,
    status=status.HTTP_200_OK)

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
# ENDPOINT personalizado para confirmar reservas

