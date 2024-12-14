from django.core.files import File
from django.shortcuts import get_object_or_404, render
from app_pri_gestion_docentes import settings
from autenticacion.models import MiPerfil, Profesor, Curso, Alumno
from datetime import datetime
import re
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
from weasyprint import HTML
import os
from datetime import datetime
from django.shortcuts import render, get_object_or_404
import re
from django.utils.timezone import now
import os
from django.contrib import messages
from django.shortcuts import redirect
from .models import *


# Create your views here.

def generar_reporte_clase(request):
    usuario = request.user
    perfil_actual = get_object_or_404(MiPerfil, user=usuario)
    tipo_usuario_actual = perfil_actual.tipo_usuario

    profesores = Profesor.objects.prefetch_related('cursos').all()

    if request.method == 'GET':
        return render(request, 'reporte_clase.html', {
            'profesores': profesores,
            'usuario_actual': usuario,
        })

    if request.method == 'POST':
        # Obtener el ID del profesor y el DNI
        profesor_id = request.POST.get('profesor', '').strip()
        unidad_didactica_id = request.POST.get('cursos', '').strip()

        try:
            # Buscar el profesor por su ID
            profesor = Profesor.objects.get(id=profesor_id)
            dni_profesor = profesor.dni  # Obtener el DNI del profesor
            # O el campo que almacene el nombre completo del profesor
            nombre_docente = profesor.nombre_completo
            # Buscar el curso por su ID
            unidad_didactica = Curso.objects.get(id=unidad_didactica_id)
            nombre_unidad_didactica = unidad_didactica.nombre_curso
            codigo_unidad_didactica = unidad_didactica.codigo_curso

        except ObjectDoesNotExist:
            dni_profesor = '00000000'  # Valor por defecto en caso de error
            nombre_docente = 'Profesor no encontrado'
            nombre_unidad_didactica = 'ID de curso no proporcionado'

        # Datos que se usarán en el reporte
        datos_reporte = {
            'nombre_docente': nombre_docente.upper(),
            'dni': dni_profesor,
            'fecha': datetime.now().strftime("%d/%m/%Y"),
            'nrc': request.POST.get('NRC', '').strip(),
            'unidad_didactica': nombre_unidad_didactica.upper(),
            'ciclo': request.POST.get('CICLO', '').strip(),
            'nombres_del_observador': request.POST.get('NOMBRE_DEL_SUPERVISOR', '').strip().upper(),
            'sugerencias_del_observador': request.POST.get('SUGERENCIAS_DEL_OBSERVADOR', '').strip(),
            'pregunta_1': re.sub(r'_\d+|_', '', request.POST.get('pregunta_1', '')).upper(),
            'pregunta_2': re.sub(r'_\d+|_', '', request.POST.get('pregunta_2', '')).upper(),
            'pregunta_3': re.sub(r'_\d+|_', '', request.POST.get('pregunta_3', '')).upper(),
            'pregunta_4': re.sub(r'_\d+|_', '', request.POST.get('pregunta_4', '')).upper(),
            'pregunta_5': re.sub(r'_\d+|_', '', request.POST.get('pregunta_5', '')).upper(),
            'pregunta_6': re.sub(r'_\d+|_', '', request.POST.get('pregunta_6', '')).upper(),
            'pregunta_7': re.sub(r'_\d+|_', '', request.POST.get('pregunta_7', '')).upper(),
            'pregunta_8': re.sub(r'_\d+|_', '', request.POST.get('pregunta_8', '')).upper(),
            'pregunta_9': re.sub(r'_\d+|_', '', request.POST.get('pregunta_9', '')).upper(),
            'pregunta_10': re.sub(r'_\d+|_', '', request.POST.get('pregunta_10', '')).upper(),
            'pregunta_11': re.sub(r'_\d+|_', '', request.POST.get('pregunta_11', '')).upper(),
            'pregunta_12': re.sub(r'_\d+|_', '', request.POST.get('pregunta_12', '')).upper(),
            'pregunta_13': re.sub(r'_\d+|_', '', request.POST.get('pregunta_13', '')).upper(),
            'pregunta_14': re.sub(r'_\d+|_', '', request.POST.get('pregunta_14', '')).upper(),
            'pregunta_15': re.sub(r'_\d+|_', '', request.POST.get('pregunta_15', '')).upper(),
            'pregunta_16': re.sub(r'_\d+|_', '', request.POST.get('pregunta_16', '')).upper(),
            'pregunta_17': re.sub(r'_\d+|_', '', request.POST.get('pregunta_17', '')).upper(),
        }

        # Generar el archivo PDF
        html_string = render_to_string('plantilla_reporte_clase.html', datos_reporte)

        fecha_actual = now().strftime("%Y%m%d")  # Obtener la fecha y hora actual
        nombre_pdf = f"REPORTE_CLASE_{dni_profesor}_{fecha_actual}_{codigo_unidad_didactica}.pdf"

        # Definir la ruta para guardar el archivo PDF
        output_pdf_path = os.path.join(settings.MEDIA_ROOT, 'pdf_reportes_clase', nombre_pdf)

        # Crear el PDF
        HTML(string=html_string).write_pdf(output_pdf_path)

        # Guardar la ruta del archivo PDF en el modelo ReporteClase
        reporte = ReporteClase.objects.create(
            profesor=profesor,
            archivo_pdf=f'pdf_reportes_clase/{nombre_pdf}',
        )

        # Mostrar un mensaje de éxito
        messages.success(request, f'El PDF del profesor {nombre_docente} se generó correctamente.')

        # Limpiar el formulario (si es necesario) y redirigir a la misma vista o a otra
        return redirect('reporte_clase')


    return render(request, 'reporte_clase.html', {
        'profesores': profesores,
        'usuario_actual': usuario,
    })


def generar_reporte_docente(request):
    usuario = request.user
    perfil_actual = get_object_or_404(MiPerfil, user=usuario)
    tipo_usuario_actual = perfil_actual.tipo_usuario
    print(f'tipo_usuario_actual para reporte docente: {tipo_usuario_actual}')

    profesores = Profesor.objects.prefetch_related('cursos').all()
    
    print(request.POST)
    
    if request.method == 'GET':
        return render(request, 'reporte_docente.html', {
            'profesores': profesores,
            'usuario_actual': usuario,
        })

    if request.method == 'POST':
        # Obtener el ID del profesor y el DNI
        profesor_id = request.POST.get('profesor', '').strip()
        # unidad_didactica_id = request.POST.get('cursos', '').strip()

        try:
            # Buscar el profesor por su ID
            profesor = Profesor.objects.get(id=profesor_id)
            dni_profesor = profesor.dni  # Obtener el DNI del profesor
            # O el campo que almacene el nombre completo del profesor
            nombre_docente = profesor.nombre_completo

        except ObjectDoesNotExist:
            dni_profesor = '00000000'  # Valor por defecto en caso de error
            nombre_docente = 'Profesor no encontrado'

        # Datos que se usarán en el reporte
        datos_reporte = {
            'nombre_docente': nombre_docente.upper(),
            'dni': dni_profesor,
            'fecha': datetime.now().strftime("%d/%m/%Y"),
            'ciclo': request.POST.get('CICLO', '').strip(),
            'nombres_del_observador': request.POST.get('NOMBRE_DEL_SUPERVISOR', '').strip().upper(),
            'pregunta_1': re.sub(r'_\d+|_', '', request.POST.get('pregunta_1', '')).upper(),
            'pregunta_2': re.sub(r'_\d+|_', '', request.POST.get('pregunta_2', '')).upper(),
            'pregunta_3': re.sub(r'_\d+|_', '', request.POST.get('pregunta_3', '')).upper(),
            'pregunta_4': re.sub(r'_\d+|_', '', request.POST.get('pregunta_4', '')).upper(),
            'pregunta_5': re.sub(r'_\d+|_', '', request.POST.get('pregunta_5', '')).upper(),
            'pregunta_6': re.sub(r'_\d+|_', '', request.POST.get('pregunta_6', '')).upper(),
            'pregunta_7': re.sub(r'_\d+|_', '', request.POST.get('pregunta_7', '')).upper(),
            'pregunta_8': re.sub(r'_\d+|_', '', request.POST.get('pregunta_8', '')).upper(),
            'pregunta_9': re.sub(r'_\d+|_', '', request.POST.get('pregunta_9', '')).upper(),
            'pregunta_10': re.sub(r'_\d+|_', '', request.POST.get('pregunta_10', '')).upper(),
            'pregunta_11': re.sub(r'_\d+|_', '', request.POST.get('pregunta_11', '')).upper(),
            'pregunta_12': re.sub(r'_\d+|_', '', request.POST.get('pregunta_12', '')).upper(),
            'pregunta_13': re.sub(r'_\d+|_', '', request.POST.get('pregunta_13', '')).upper(),
            'pregunta_14': re.sub(r'_\d+|_', '', request.POST.get('pregunta_14', '')).upper(),
            'pregunta_15': re.sub(r'_\d+|_', '', request.POST.get('pregunta_15', '')).upper(),
        }
        
        print(f'datos_reporte: {datos_reporte}')

        # Generar el archivo PDF
        html_string = render_to_string('plantilla_reporte_docente.html', datos_reporte)

        fecha_actual = now().strftime("%Y%m%d")  # Obtener la fecha y hora actual
        nombre_pdf = f"REPORTE_DOCENTE_{dni_profesor}_{fecha_actual}.pdf"

        # Definir la ruta para guardar el archivo PDF
        output_pdf_path = os.path.join(settings.MEDIA_ROOT, 'pdf_reportes_docente', nombre_pdf)

        # Crear el PDF
        HTML(string=html_string).write_pdf(output_pdf_path)

        # Guardar la ruta del archivo PDF en el modelo ReporteClase
        reporte = ReporteDocente.objects.create(
            profesor=profesor,
            archivo_pdf=f'pdf_reportes_docente/{nombre_pdf}',
        )

        # Mostrar un mensaje de éxito
        messages.success(request, f'El PDF del profesor {nombre_docente} se generó correctamente.')

        # Limpiar el formulario (si es necesario) y redirigir a la misma vista o a otra
        return redirect('reporte_docente')


    return render(request, 'reporte_docente.html', {
        'profesores': profesores,
        'usuario_actual': usuario,
    })