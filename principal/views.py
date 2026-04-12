from django.shortcuts import get_object_or_404, render

from principal.models import DisponibilidadSala, Grupo, Sala

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
