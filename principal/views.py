from django.shortcuts import get_object_or_404, render

from principal.models import DisponibilidadSala, Grupo, Sala
from django.shortcuts import render
from .models import Sala
from django.db.models import Q

# Create your views here.

def index(request):
    return render(request, 'principal/index.html')
# vista para listar todas las salas
def listado_salas(request):
    salas = Sala.objects.all()
    return render(request, 'principal/listado_salas.html', {'salas': salas})

# vistas para ver la disponibilidad de una sala
def fechas_disponibles_view(request, sala_id):
    sala = get_object_or_404(Sala, id=sala_id)
    fechas_disponibles = DisponibilidadSala.objects.filter(
        estado='disponible',
        sala=sala
    ).order_by('fecha')
    
    return render(request, 'principal/fechas_disponibles.html', {
        'sala': sala,
        'fechas_disponibles': fechas_disponibles
    })
# vista para ver todos los grupos
def listado_grupos(request):
    grupos = Grupo.objects.all()
    return render(request, 'principal/listado_grupos.html', {'grupos': grupos})
# vista para que se vea la informacion publica de la cuenta del grupo o sala
def cuenta_publica_grupos(request, id):
    grupo = get_object_or_404(Grupo, id=id)
    return render(request, 'principal/cuenta_publica_grupos.html', {'grupo': grupo})
def cuenta_publica_salas(request, id):
    sala = get_object_or_404(Sala, id=id)
    return render(request, 'principal/cuenta_publica_salas.html', {'sala': sala})
# vista de busqueda sala por ciudad o nombre con htmx
def buscar(request):
    q = request.GET.get('q', '')

    salas = Sala.objects.none()
    grupos = Grupo.objects.none()

    if q:
        salas = Sala.objects.filter(
            Q(nombre__icontains=q) |
            Q(ciudad__icontains=q)
        )

        grupos = Grupo.objects.filter(
            Q(nombre__icontains=q) |
            Q(ciudad__icontains=q)
        )

    return render(request, 'principal/partials/lista_busqueda.html', {
        'salas': salas,
        'grupos': grupos,
        'query': q
    })
def buscador(request):
    return render(request, 'principal/buscador.html')