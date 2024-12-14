from django.urls import path
from .views import (
    inicio_sesion,
    crear_cuenta,
    cerrar_sesion,
    perfil_usuario_actual,
    perfil_usuario,
)

urlpatterns = [
    path('inicio_sesion/', inicio_sesion, name='inicio_sesion'),
    path('crear_cuenta/', crear_cuenta, name='crear_cuenta'),
    path('cerrar_sesion/', cerrar_sesion, name='cerrar_sesion'),
    path('perfil/', perfil_usuario_actual, name='perfil_usuario_actual'),
    path('perfil/<int:user_id>/', perfil_usuario, name='perfil_usuario'),
]