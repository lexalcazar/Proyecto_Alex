from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    ROLES = [
        ('usuario', 'Usuario'),
        ('grupo', 'Grupo'),
        ('sala', 'Sala'),
    ]

    rol = models.CharField(max_length=20, choices=ROLES, default='usuario')

    def __str__(self):
        return self.username


class Sala(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=100)
    aforo = models.IntegerField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    redes_sociales = models.TextField(blank=True, null=True)
    imagen = models.ImageField(upload_to='salas/', blank=True, null=True)
    rider = models.TextField(blank=True, null=True)
    email_contacto = models.EmailField()
    telefono_contacto = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.nombre


class Grupo(models.Model):
    nombre = models.CharField(max_length=100)
    genero = models.CharField(max_length=100, blank=True, null=True)
    integrantes = models.IntegerField()
    biografia = models.TextField(blank=True, null=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    redes_sociales = models.TextField(blank=True, null=True)
    imagen = models.ImageField(upload_to='grupos/', blank=True, null=True)
    rider = models.TextField(blank=True, null=True)
    ciudad = models.CharField(max_length=100)
    email_contacto = models.EmailField()
    telefono_contacto = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.nombre


class DisponibilidadSala(models.Model):
    ESTADOS = [
        ('disponible', 'Disponible'),
        ('reservado', 'Reservado'),
        ('cerrado', 'Cerrado'),
    ]

    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    fecha = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='disponible')

    def __str__(self):
        return f"{self.sala.nombre} - {self.fecha} - {self.estado}"


class Reserva(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    ]

    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    fecha_reserva = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    mensaje_grupo = models.TextField(blank=True, null=True)
    respuesta_sala = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.grupo.nombre} - {self.sala.nombre} - {self.fecha_reserva} - {self.estado}"


class Evento(models.Model):
    reserva = models.OneToOneField(Reserva, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=150)
    fecha_evento = models.DateField()
    descripcion = models.TextField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f"{self.nombre} - {self.fecha_evento}"