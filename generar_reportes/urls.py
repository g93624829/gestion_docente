from django.urls import path
from .views import *

urlpatterns = [
    path('reporte_clase/', generar_reporte_clase, name='reporte_clase'),
    path('reporte_docente/', generar_reporte_docente, name='reporte_docente'),
]