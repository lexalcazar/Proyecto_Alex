
from rest_framework import serializers
from django.contrib.auth.decorators import login_required
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

# ver
class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sala
        fields = ['id', 'nombre', 'direccion', 'ciudad', 'aforo', 'usuario', 'redes_sociales', 'imagen', 'rider', 'email_contacto', 'telefono_contacto']

# crear
class CreateSalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sala
        fields = ['nombre', 'direccion', 'ciudad', 'aforo', 'usuario', 'redes_sociales', 'imagen', 'rider', 'email_contacto', 'telefono_contacto']
    def create(self, validated_data):
        return Sala.objects.create(**validated_data)
    
# Serializadores para los Grupos 

# ver
class GrupoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grupo
        fields = ['id', 'nombre', 'genero', 'integrantes', 'biografia', 'usuario', 'redes_sociales', 'imagen', 'rider', 'ciudad', 'email_contacto', 'telefono_contacto']
# crear

class CreateGrupoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grupo
        fields = ['nombre', 'genero', 'integrantes', 'biografia', 'usuario', 'redes_sociales', 'imagen', 'rider', 'ciudad', 'email_contacto', 'telefono_contacto']
    def create(self, validated_data):
        return Grupo.objects.create(**validated_data)
     
# Serializadores para la Disponibilidad de las Salas
class DisponibilidadSalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisponibilidadSala
        fields = ['id', 'sala', 'fecha', 'estado']
class CreateDisponibilidadSalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisponibilidadSala
        fields = ['sala', 'fecha', 'estado']
    def create(self, validated_data):
        return DisponibilidadSala.objects.create(**validated_data)
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