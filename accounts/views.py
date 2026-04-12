from django.utils import timezone
from django.shortcuts import get_object_or_404, render

from principal.models import Sala, Grupo
from .forms import LoginForm, RegistroForm
# Create your views here.

# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def contador_visitas(request):
    """
    Demuestra el uso de sesiones sin autenticación.
    Cada visitante anónimo obtiene un contador persistente vía cookie.
    """
    # Obtener contador actual de la sesión (o 0 si no existe)
    visitas = request.session.get('contador_visitas', 0)
    
    # Incrementar y guardar
    visitas += 1
    request.session['contador_visitas'] = visitas
    
    # Guardar timestamp de primera visita
    if visitas == 1:
        request.session['primera_visita'] = str(timezone.now())
    
    return render(request, 'accounts/contador.html', {
        'visitas': visitas,
        'session_id': request.session.session_key,
        'primera_visita': request.session.get('primera_visita'),
    })

def login_view(request):
    """
    Vista de login personalizada.
    Maneja autenticación y configuración de sesión.
    """
    if request.user.is_authenticated:
        return redirect('perfil')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Gestión de "Recordarme"
            if not form.cleaned_data.get('remember_me'):
                # Sesión expira al cerrar navegador
                request.session.set_expiry(0)
            else:
                # Usar duración por defecto (2 semanas)
                request.session.set_expiry(None)
            
            messages.success(request, f'¡Bienvenido, {user.username}!')
            
            # Redirigir a página solicitada originalmente (o perfil por defecto)
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('cuenta')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """Cierra sesión y elimina la cookie de sesión"""
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('login')


def registro_view(request):
    """Registro de nuevos usuarios"""
    if request.user.is_authenticated:
        return redirect('perfil')
        
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Cuenta creada. Ahora puedes iniciar sesión.')
            return redirect('login')
    else:
        form = RegistroForm()
    
    return render(request, 'accounts/registro.html', {'form': form})


@login_required
def perfil_view(request):
    """
    Vista protegida: solo usuarios autenticados.
    El decorador @login_required verifica la sesión automáticamente.
    """
    # Información de la sesión actual
    session_info = {
        'session_key': request.session.session_key,
        'fecha_expiracion': request.session.get_expiry_date(),
        'tiempo_restante': request.session.get_expiry_age(),
    }
    
    return render(request, 'accounts/perfil.html', {
        'session_info': session_info,
        'user': request.user,
    })
#Una vez logueado el usuario accede a su cuenta
# se redirige a cuenta.html
# si su rol es de grupo se vera el grupo que tiene asignado
# si su rol es de sala se vera la sala que tiene asignada
def cuenta_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    user = request.user
    context = {'user': user}
    
    if user.rol == 'grupo':
        # Obtener grupo asociado al usuario
        grupo = Grupo.objects.filter(usuario=user).first()
        context['grupo'] = grupo
    elif user.rol == 'sala':
        # Obtener sala asociada al usuario
        sala = Sala.objects.filter(usuario=user).first()
        context['sala'] = sala
    
    return render(request, 'principal/cuenta.html', context)

