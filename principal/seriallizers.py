
from rest_framework import serializers

from principal.models import DisponibilidadSala, Grupo, Sala, Usuario

class UsuarioSerializer(serializers.Serializer):
   class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'rol']

class SalaSerializer(serializers.Serializer):
    class Meta:
        model = Sala
        fields = ['id', 'nombre', 'direccion', 'ciudad', 'aforo', 'usuario', 'redes_sociales', 'imagen', 'rider', 'email_contacto', 'telefono_contacto']

class GrupoSerializer(serializers.Serializer):
    class Meta:
        model = Grupo
        fields = ['id', 'nombre', 'genero', 'integrantes', 'biografia', 'usuario', 'redes_sociales', 'imagen', 'rider', 'ciudad', 'email_contacto', 'telefono_contacto']

class DisponibilidadSalaSerializer(serializers.Serializer):
    class Meta:
        model = DisponibilidadSala
        fields = ['id', 'sala', 'fecha', 'estado']

class ReservaSerializer(serializers.Serializer):
    class Meta:
        model = DisponibilidadSala
        fields = ['id', 'sala', 'fecha', 'estado']

class EventoSerializer(serializers.Serializer):
    class Meta:
        model = DisponibilidadSala
        fields = ['id', 'sala', 'fecha', 'estado']