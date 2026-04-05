
from rest_framework import serializers

from principal.models import DisponibilidadSala, Grupo, Sala, Usuario
# Serializadores para los Usuarios
class UsuarioSerializer(serializers.ModelSerializer):
   class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'rol']
class CreateUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['first_name','last_name','username', 'email', 'password', 'rol']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return Usuario.objects.create_user(**validated_data)
# Serializadores para las Salas
class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sala
        fields = ['id', 'nombre', 'direccion', 'ciudad', 'aforo', 'usuario', 'redes_sociales', 'imagen', 'rider', 'email_contacto', 'telefono_contacto']
class CreateSalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sala
        fields = ['nombre', 'direccion', 'ciudad', 'aforo', 'usuario', 'redes_sociales', 'imagen', 'rider', 'email_contacto', 'telefono_contacto']
    def create(self, validated_data):
        return Sala.objects.create(**validated_data)
# Serializadores para los Grupos 
class GrupoSerializer(serializers.Serializer):
    class Meta:
        model = Grupo
        fields = ['id', 'nombre', 'genero', 'integrantes', 'biografia', 'usuario', 'redes_sociales', 'imagen', 'rider', 'ciudad', 'email_contacto', 'telefono_contacto']
    
# Serializadores para la Disponibilidad de las Salas
class DisponibilidadSalaSerializer(serializers.Serializer):
    class Meta:
        model = DisponibilidadSala
        fields = ['id', 'sala', 'fecha', 'estado']
# Serializadores para las Reservas
class ReservaSerializer(serializers.Serializer):
    class Meta:
        model = DisponibilidadSala
        fields = ['id', 'sala', 'fecha', 'estado']
# Serializadores para los Eventos
class EventoSerializer(serializers.Serializer):
    class Meta:
        model = DisponibilidadSala
        fields = ['id', 'sala', 'fecha', 'estado']