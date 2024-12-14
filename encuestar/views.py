from django.shortcuts import render
from autenticacion.models import Profesor, Alumno, MiPerfil
from .models import Encuesta


def encuestar(request):
    tipo_usuario = "No especificado"
    profesores = []

    if request.user.is_authenticated:
        try:
            # Buscar el perfil asociado al usuario autenticado
            perfil = MiPerfil.objects.get(user=request.user)
            tipo_usuario = perfil.tipo_usuario
        except MiPerfil.DoesNotExist:
            pass  # Mantener el valor predeterminado si no existe un perfil

        # Obtener todos los usuarios con tipo_usuario "profesor(a)"
        profesores = Profesor.objects.all()

    if request.method == "POST":
        profesor_id = request.POST.get('profesor')  # Cambié 'docente' por 'profesor'
        print("ID del usuario (profesor_id):", profesor_id)
        print("Respuestas:", request.POST.get('pregunta1'), request.POST.get('pregunta2'), request.POST.get('pregunta3'), request.POST.get('pregunta4'), request.POST.get('pregunta5'))

        # Verificar si alguna pregunta está vacía
        pregunta1 = request.POST.get('pregunta1')
        pregunta2 = request.POST.get('pregunta2')
        pregunta3 = request.POST.get('pregunta3')
        pregunta4 = request.POST.get('pregunta4')
        pregunta5 = request.POST.get('pregunta5')

        # Verificar si alguna respuesta está vacía
        if not all([pregunta1, pregunta2, pregunta3, pregunta4, pregunta5]):
            mensaje = "Por favor, responde todas las preguntas de la encuesta."
            return render(request, 'encuestar.html', {
                'mensaje': mensaje,
                'tipo_usuario': tipo_usuario,
                'usuario_actual': request.user,
                'profesores': profesores,
            })

        try:
            # Buscar al Profesor usando el profesor_id
            profesor = Profesor.objects.get(id=profesor_id)
        except Profesor.DoesNotExist:
            print(f"No se encontró el profesor con id {profesor_id}")
            mensaje = "Profesor no encontrado"
            return render(request, 'encuestar.html', {
                'mensaje': mensaje,
                'tipo_usuario': tipo_usuario,
                'usuario_actual': request.user,
                'profesores': profesores,
            })

        # Obtener el alumno (usuario autenticado)
        try:
            alumno = Alumno.objects.get(user=request.user)
        except Alumno.DoesNotExist:
            print(f"No se encontró el alumno asociado al usuario {request.user.username}")
            mensaje = "No se encontró el alumno"
            return render(request, 'encuestar.html', {
                'mensaje': mensaje,
                'tipo_usuario': tipo_usuario,
                'usuario_actual': request.user,
                'profesores': profesores,
            })

        # Verificar si ya existe una encuesta del alumno hacia el profesor
        encuesta_existente = Encuesta.objects.filter(alumno=alumno, profesor=profesor).exists()

        if encuesta_existente:
            mensaje = f"Ya has enviado una encuesta al profesor(a) {(profesor.nombre_completo).upper()}"
            # Volver a mostrar la lista de profesores pero deshabilitar el que ya fue encuestado
            return render(request, 'encuestar.html', {
                'mensaje': mensaje,
                'tipo_usuario': tipo_usuario,
                'usuario_actual': request.user,
                'profesores': profesores,
                'profesor_encuestado': profesor_id,  # Indicamos que este profesor ya fue encuestado
            })

        # Guardar las respuestas en la base de datos
        encuesta = Encuesta(
            alumno=alumno,  # El objeto completo de Alumno
            profesor=profesor,  # El objeto completo de Profesor
            pregunta1=pregunta1,
            pregunta2=pregunta2,
            pregunta3=pregunta3,
            pregunta4=pregunta4,
            pregunta5=pregunta5
        )
        encuesta.save()

        # Mensaje de éxito
        mensaje = "Encuesta enviada con éxito"
        return render(request, 'encuestar.html', {
            'mensaje': mensaje,
            'tipo_usuario': tipo_usuario,
            'usuario_actual': request.user,
            'profesores': profesores,
        })

    # Si la petición es GET, renderizamos la página con los profesores
    return render(request, 'encuestar.html', {
        'tipo_usuario': tipo_usuario,
        'usuario_actual': request.user,
        'profesores': profesores,
    })