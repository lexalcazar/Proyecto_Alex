
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.contrib.auth.decorators import login_required
from principal.models import DisponibilidadSala, Evento, Grupo, Reserva, Sala, Usuario
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
        fields = ['nombre', 'genero', 'integrantes', 'biografia', 'redes_sociales', 'imagen', 'rider', 'ciudad', 'email_contacto', 'telefono_contacto']
        
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
class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = '__all__'
# crear pero la fecha de reserva viene de disponibilidad sala donde fecha=disponible
class CreateReservaSerializer(serializers.ModelSerializer):
    disponibilidad = serializers.PrimaryKeyRelatedField(
        queryset=DisponibilidadSala.objects.filter(estado='disponible'),
        write_only=True
    )

    class Meta:
        model = Reserva
        fields = ['disponibilidad', 'mensaje_grupo']  # 👈 limpio

    def validate(self, data):
        disponibilidad = data.get('disponibilidad')

        if disponibilidad.estado != 'disponible':
            raise serializers.ValidationError(
                "La sala no está disponible en la fecha seleccionada."
            )

        data['sala'] = disponibilidad.sala
        data['fecha_reserva'] = disponibilidad.fecha
        return data

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        # 🔥 AQUÍ está la clave
        grupo = get_object_or_404(Grupo, usuario=user)   # o como lo tengas definido

        disponibilidad = validated_data.pop('disponibilidad')

        reserva = Reserva.objects.create(
            grupo=grupo,
            estado='pendiente',
            confirmacion_sala=False,
            **validated_data
        )

        disponibilidad.estado = 'pendiente'
        disponibilidad.save()

        return reserva
#Seriallizer para confirmar la reserva por parte de la sala, se actualiza el estado de la reserva a confirmada y la disponibilidad a reservado
class ConfirmarReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = ['id', 'confirmacion_sala']
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        confirmacion_sala = validated_data.get('confirmacion_sala')

        instance.confirmacion_sala = confirmacion_sala

        disponibilidad = get_object_or_404(
            DisponibilidadSala,
            sala=instance.sala,
            fecha=instance.fecha_reserva
        )

        if confirmacion_sala:
            instance.estado = 'confirmada'
            disponibilidad.estado = 'reservado'
        else:
            instance.estado = 'rechazada'
            disponibilidad.estado = 'disponible'

        instance.save()
        disponibilidad.save()

        return instance
class ConfirmacionReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields =  ['id', 'confirmacion_sala', 'estado'] 

# Serializadores para los Eventos
class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = '__all__'
class CreateEventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = '__all__'
    def create(self, validated_data):
        return Evento.objects.create(**validated_data)