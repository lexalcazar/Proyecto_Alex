from rest_framework import viewsets
from rest_framework.response import Response
from principal.models import Sala, Usuario
from principal.seriallizers import CreateSalaSerializer, CreateSalaSerializer, CreateUsuarioSerializer, SalaSerializer, SalaSerializer, UsuarioSerializer
from rest_framework.decorators import api_view

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    def get_serializer_class(self):
        """Usa diferente serializer según la acción"""
        if self.action in ['create', 'update', 'partial_update']:
            return CreateUsuarioSerializer
        return UsuarioSerializer

class SalaViewSet(viewsets.ModelViewSet):
    queryset = Sala.objects.all()
    def get_serializer_class(self):
        """Usa diferente serializer según la acción"""
        if self.action in ['create', 'update', 'partial_update']:
            return CreateSalaSerializer
        return SalaSerializer

# patrones personalizados

@api_view(['GET'])
def salas_por_ciudad(request, ciudad):
    """Devuelve las salas filtradas por ciudad"""
    salas = Sala.objects.filter(ciudad=ciudad)
    serializer = SalaSerializer(salas, many=True)
    return Response(serializer.data)