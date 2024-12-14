from django.shortcuts import render
from django.shortcuts import render
from autenticacion.models import *

# Create your views here.
def pagina_principal(request):
    tipo_usuario = None
    usuarios = User.objects.all()

    if request.user.is_authenticated:
        try:
            # Buscar el perfil asociado al usuario autenticado
            perfil = MiPerfil.objects.get(user=request.user)
            tipo_usuario = perfil.tipo_usuario
        except MiPerfil.DoesNotExist:
            tipo_usuario = "No especificado"  # Valor por defecto si no existe un perfil

    # Pasar el dato `tipo_usuario` al template
    return render(request, 'pagina_principal.html', {
        'tipo_usuario': tipo_usuario,
        'usuarios': usuarios,
        })