import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import Http404
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from .models import *
from .forms import *
from encuestar.models import *
from generar_reportes.models import *

# Create your views here.
def inicio_sesion(request):
    if request.method == 'GET':
        return render(request, 'inicio_sesion.html', {'form': AuthenticationForm()})

    elif request.method == 'POST':
        email = request.POST.get('email', '').lower()
        password = request.POST.get('password', '')

        try:
            # Buscar al usuario por correo
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user and user.check_password(password):
            login(request, user)
            return redirect('pagina_principal')
        else:
            return render(request, 'inicio_sesion.html', {
                'form': AuthenticationForm(),
                'error': 'Correo o contraseña incorrectos.'
            })


def cerrar_sesion(request):
    logout(request)
    return redirect('pagina_principal')

@login_required
def crear_cuenta(request):
    usuario = request.user  # Obtienes el usuario autenticado
    perfil_actual = get_object_or_404(MiPerfil, user=usuario)
    tipo_usuario_actual = perfil_actual.tipo_usuario
    print(f'tipo_usuario_actual para crear cuenta: {tipo_usuario_actual}')
    
    if request.method == 'GET':
        return render(request, 'crear_cuenta.html', {
            'form': UserCreationForm(),
            'tipo_usuario_actual': tipo_usuario_actual,
        })

    if request.method == 'POST':
        # Obtener datos del formulario
        print(request.POST)

        form_data = {
            'tipo_usuario': request.POST.get('tipo_usuario', '').lower(),
            'nombres': request.POST.get('nombres', '').lower(),
            'apellidop': request.POST.get('apellidop', '').lower(),
            'apellidom': request.POST.get('apellidom', '').lower(),
            'dni': request.POST.get('dni', '').strip(),
            'email': request.POST.get('email', '').lower(),
            'password1': request.POST.get('password1', '').strip(),
            'password2': request.POST.get('password2', '').strip(),
        }
        
        # Validar DNI con RENIEC
        is_valid, nombre_lista_reniec = validate_dni(form_data['dni'])
        print(f'is_valid: {is_valid}')
        print(f'nombre_lista_reniec: {nombre_lista_reniec}')
        if not is_valid:
            return render(request, 'crear_cuenta.html', {
                'form': UserCreationForm(),
                'error': 'DNI no válido',
            })
        
        # Construir nombre completo
        apellido_paterno, apellido_materno, nombres_reniec = map(str.lower, nombre_lista_reniec)
        nombre_reniec = f"{apellido_paterno} {apellido_materno} {nombres_reniec}"
        nombre_completo = f"{form_data['apellidop']} {form_data['apellidom']} {form_data['nombres']}".lower()
        nombre_completo_ordenado = f"{form_data['nombres']} {form_data['apellidop']} {form_data['apellidom']}".lower()
        
        # Tipo de Usuario = Alumno
        if form_data['tipo_usuario'] == "alumno(a)":
            correo_edu = f"{form_data['dni']}@certus.edu.pe"
            print(f'correoedu: {correo_edu}')
            print(f'correo: {form_data["email"]}')
            carrera_codigo = request.POST.get('carrera')
            print(f"prueba carrera: {carrera_codigo}")
            carrera = get_object_or_404(Carrera, codigo_carrera=carrera_codigo)
            print(f"prueba carrera: {carrera}")
            
            # Validaciones de formulario
            errors = []
            
            if len(form_data['dni']) != 8 or not form_data['dni'].isdigit():
                errors.append('El DNI debe tener 8 dígitos y ser numérico.')

            if nombre_completo != nombre_reniec:
                errors.append(
                    'Los nombres y apellidos no coinciden con los datos de RENIEC.')

            if form_data['email'] != correo_edu:
                errors.append('El correo institucional no coincide.')

            if form_data['password1'] != form_data['password2']:
                errors.append('Las contraseñas no coinciden.')

            if errors:
                return render(request, 'crear_cuenta.html', {
                    'form': UserCreationForm(),
                    'error': ' '.join(errors),
                })
            
            # Crear usuario si no hay errores
            try:
                user = User.objects.create_user(
                    username=nombre_completo_ordenado,
                    email=correo_edu,
                    password=form_data['password1'],
                    first_name=form_data['nombres'],
                    last_name=f"{form_data['apellidop']} {form_data['apellidom']}",
                )

                # Crear perfil adicional
                MiPerfil.objects.create(
                    user=user,
                    dni=form_data['dni'],
                    tipo_usuario=form_data['tipo_usuario'],
                    correo_electronico=form_data['email'],
                    nombre_usuario=nombre_completo_ordenado,
                )
                
                Alumno.objects.create(
                    user=user,
                    dni=form_data['dni'],
                    correo_electronico=form_data['email'],
                    nombre_completo=nombre_completo_ordenado,
                    carrera=carrera,
                    nombres=form_data['nombres'],
                    apellido_paterno=form_data['apellidop'],
                    apellido_materno=form_data['apellidom'],
                    tipo_usuario=form_data['tipo_usuario'],
                )
                # Iniciar sesión y redirigir
                # login(request, user)
                # return redirect('pagina_principal')
                mensaje_de_confirmacion = "Usuario creado exitosamente"
                correo_creado_exitosamente = form_data['email']
                contrasenia_creada_exitosamente = form_data['password1']
                return render(request, 'crear_cuenta.html', {
                    # 'form': UserCreationForm(),
                    'mensaje_de_confirmacion': mensaje_de_confirmacion,
                    'correo_creado_exitosamente': correo_creado_exitosamente,
                    'contrasenia_creada_exitosamente': contrasenia_creada_exitosamente,
                })

            except IntegrityError:
                return render(request, 'crear_cuenta.html', {
                    'form': UserCreationForm(),
                    'error': 'El nombre de usuario o correo ya existe.',
                    'mensaje_de_confirmacion': mensaje_de_confirmacion,
                })

        # Tipo de Usuario = Profesor
        elif form_data['tipo_usuario'] == "profesor(a)":
            correo_edu = f"{nombres_reniec[0]}{apellido_paterno}{apellido_materno[0]}@certus.edu.pe"
            print(f'correoedu: {correo_edu}')
            print(f'correo: {form_data["email"]}')
            cursos_codigos = request.POST.getlist('cursos[]')
            print(f"prueba curso: {cursos_codigos}")
            
            # Validaciones de formulario
            errors = []
            if len(form_data['dni']) != 8 or not form_data['dni'].isdigit():
                errors.append('El DNI debe tener 8 dígitos y ser numérico.')

            if nombre_completo != nombre_reniec:
                errors.append(
                    'Los nombres y apellidos no coinciden con los datos de RENIEC.')

            if form_data['email'] != correo_edu:
                errors.append('El correo institucional no coincide.')

            if form_data['password1'] != form_data['password2']:
                errors.append('Las contraseñas no coinciden.')

            if errors:
                return render(request, 'crear_cuenta.html', {
                    'form': UserCreationForm(),
                    'error': ' '.join(errors),
                })
            
            # Crear usuario si no hay errores
            try:
                user = User.objects.create_user(
                    username=nombre_completo_ordenado,
                    email=correo_edu,
                    password=form_data['password1'],
                    first_name=form_data['nombres'],
                    last_name=f"{form_data['apellidop']} {form_data['apellidom']}",
                )

                # Crear perfil adicional
                MiPerfil.objects.create(
                    user=user,
                    dni=form_data['dni'],
                    tipo_usuario=form_data['tipo_usuario'],
                    correo_electronico=form_data['email'],
                    nombre_usuario=nombre_completo_ordenado,
                )

                # Crear el profesor
                profesor = Profesor.objects.create(
                    user=user,
                    dni=form_data['dni'],
                    correo_electronico=form_data['email'],
                    nombre_completo=nombre_completo_ordenado,
                    nombres=form_data['nombres'],
                    apellido_paterno=form_data['apellidop'],
                    apellido_materno=form_data['apellidom'],
                    tipo_usuario=form_data['tipo_usuario'],
                )

                # Asignar cursos al profesor
                cursos_codigos = request.POST.getlist('cursos[]')
                cursos = Curso.objects.filter(codigo_curso__in=cursos_codigos)
                print(f'cursos de asignacion prueba: {cursos}')
                profesor.cursos.set(cursos)

                # Iniciar sesión y redirigir
                # login(request, user)
                # return redirect('pagina_principal')
                mensaje_de_confirmacion = "Usuario creado exitosamente"
                correo_creado_exitosamente = form_data['email']
                contrasenia_creada_exitosamente = form_data['password1']
                return render(request, 'crear_cuenta.html', {
                    # 'form': UserCreationForm(),
                    'mensaje_de_confirmacion': mensaje_de_confirmacion,
                    'correo_creado_exitosamente': correo_creado_exitosamente,
                    'contrasenia_creada_exitosamente': contrasenia_creada_exitosamente,
                })

            except IntegrityError:
                return render(request, 'crear_cuenta.html', {
                    'form': UserCreationForm(),
                    'error': 'El nombre de usuario o correo ya existe.',
                    'mensaje_de_confirmacion': mensaje_de_confirmacion,
                })
                
        # Tipo de Usuario = Supervisor
        elif form_data['tipo_usuario'] == "supervisor(a)":
            correo_edu = f"{nombres_reniec[0]}{apellido_paterno}{apellido_materno[0]}@certus.edu.pe"
            print(f'correoedu: {correo_edu}')
            print(f'correo: {form_data["email"]}')
            cursos_codigos = request.POST.getlist('cursos[]')
            print(f"prueba curso: {cursos_codigos}")
            
            # Validaciones de formulario
            errors = []
            if len(form_data['dni']) != 8 or not form_data['dni'].isdigit():
                errors.append('El DNI debe tener 8 dígitos y ser numérico.')

            if nombre_completo != nombre_reniec:
                errors.append(
                    'Los nombres y apellidos no coinciden con los datos de RENIEC.')

            if form_data['email'] != correo_edu:
                errors.append('El correo institucional no coincide.')

            if form_data['password1'] != form_data['password2']:
                errors.append('Las contraseñas no coinciden.')

            if errors:
                return render(request, 'crear_cuenta.html', {
                    'form': UserCreationForm(),
                    'error': ' '.join(errors),
                })
            
            # Crear usuario si no hay errores
            try:
                user = User.objects.create_user(
                    username=nombre_completo_ordenado,
                    email=correo_edu,
                    password=form_data['password1'],
                    first_name=form_data['nombres'],
                    last_name=f"{form_data['apellidop']} {form_data['apellidom']}",
                )

                # Crear perfil adicional
                MiPerfil.objects.create(
                    user=user,
                    dni=form_data['dni'],
                    tipo_usuario=form_data['tipo_usuario'],
                    correo_electronico=form_data['email'],
                    nombre_usuario=nombre_completo_ordenado,
                )

                # Crear el supervisor
                supervisor = Supervisor.objects.create(
                    user=user,
                    dni=form_data['dni'],
                    correo_electronico=form_data['email'],
                    nombre_completo=nombre_completo_ordenado,
                    nombres=form_data['nombres'],
                    apellido_paterno=form_data['apellidop'],
                    apellido_materno=form_data['apellidom'],
                    tipo_usuario=form_data['tipo_usuario'],
                )

                # Iniciar sesión y redirigir
                # login(request, user)
                # return redirect('pagina_principal')
                mensaje_de_confirmacion = "Usuario creado exitosamente"
                correo_creado_exitosamente = form_data['email']
                contrasenia_creada_exitosamente = form_data['password1']
                return render(request, 'crear_cuenta.html', {
                    # 'form': UserCreationForm(),
                    'mensaje_de_confirmacion': mensaje_de_confirmacion,
                    'correo_creado_exitosamente': correo_creado_exitosamente,
                    'contrasenia_creada_exitosamente': contrasenia_creada_exitosamente,
                })

            except IntegrityError:
                return render(request, 'crear_cuenta.html', {
                    'form': UserCreationForm(),
                    'error': 'El nombre de usuario o correo ya existe.',
                    'mensaje_de_confirmacion': mensaje_de_confirmacion,
                })

        else:
            return render(request, 'crear_cuenta.html', {
                'form': UserCreationForm(),
                'error': 'Tipo de usuario inválido.',
            })

    # Renderizar formulario vacío como fallback
    return render(request, 'crear_cuenta.html', {'form': UserCreationForm()})


# def validate_dni(dni):
#     # Verificar si el DNI tiene 8 dígitos y es numérico
#     if len(dni) != 8 or not dni.isdigit():
#         return False, "DNI inválido: debe tener 8 dígitos"

#     # Configuración de Selenium para buscar el DNI en eldni.com
#     chrome_options = Options()
#     # Modo headless para evitar mostrar el navegador
#     chrome_options.add_argument("--headless")
#     chrome_options.add_argument("--disable-gpu")
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--disable-dev-shm-usage")
#     chrome_options.add_argument(
#         "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

#     driver = None
#     try:
#         # Inicializar el navegador
#         driver = webdriver.Chrome(options=chrome_options)
#         driver.get('https://eldni.com/')

#         # Esperar hasta que el campo de DNI esté disponible
#         WebDriverWait(driver, 10).until(
            # EC.presence_of_element_located((By.ID, 'dni'))
    #     )

    #     # Ingresar el DNI y realizar la búsqueda
    #     dni_input = driver.find_element(By.ID, 'dni')
    #     dni_input.clear()
    #     dni_input.send_keys(dni)

    #     btn_buscar = WebDriverWait(driver, 10).until(
    #         EC.element_to_be_clickable((By.ID, 'btn-buscar-datos-por-dni'))
    #     )
    #     btn_buscar.click()

    #     # Esperar a que los datos sean cargados en la página
    #     WebDriverWait(driver, 10).until(
    #         EC.presence_of_element_located((By.ID, 'nombres'))
    #     )

    #     # Extraer el contenido de la página
    #     response = driver.page_source
    #     soup = BeautifulSoup(response, 'html.parser')

    #     # Extraer los datos del formulario
    #     apellidop = soup.find('input', {'id': 'apellidop'})['value'].strip()
    #     apellidom = soup.find('input', {'id': 'apellidom'})['value'].strip()
    #     nombres = soup.find('input', {'id': 'nombres'})['value'].strip()

    #     # Verificar que los datos se hayan obtenido correctamente
    #     if not (apellidop and apellidom and nombres):
    #         return False, "No se encontraron datos válidos para el DNI ingresado"

    #     nombre_lista_reniec = [apellidop, apellidom, nombres]
    #     print(f"Datos extraídos: {nombre_lista_reniec}")
    #     return True, nombre_lista_reniec

    # except Exception as e:
    #     print(f"Error al validar DNI: {e}")
    #     return False, "Ocurrió un error al validar el DNI"

    # finally:
    #     if driver:
    #         driver.quit()



def validate_dni(dni): 
    # Verificar si el DNI tiene 8 dígitos y es numérico
    if len(dni) != 8 or not dni.isdigit():
        return False, "DNI inválido: debe tener 8 dígitos"

    # Configuración de Selenium para buscar el DNI en eldni.com
    chrome_options = Options()
    # Modo headless para evitar mostrar el navegador
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # Ruta a chromedriver
    chromedriver_path = '/usr/bin/chromedriver'

    # Inicializar el servicio de ChromeDriver
    service = Service(executable_path=chromedriver_path)

    driver = None
    try:
        # Inicializar el navegador con el servicio y las opciones
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get('https://eldni.com/')

        # Esperar hasta que el campo de DNI esté disponible
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'dni'))
        )

        # Ingresar el DNI y realizar la búsqueda
        dni_input = driver.find_element(By.ID, 'dni')
        dni_input.clear()
        dni_input.send_keys(dni)

        btn_buscar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'btn-buscar-datos-por-dni'))
        )
        btn_buscar.click()

        # Esperar a que los datos sean cargados en la página
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'nombres'))
        )

        # Extraer el contenido de la página
        response = driver.page_source
        soup = BeautifulSoup(response, 'html.parser')

        # Extraer los datos del formulario
        apellidop = soup.find('input', {'id': 'apellidop'})['value'].strip()
        apellidom = soup.find('input', {'id': 'apellidom'})['value'].strip()
        nombres = soup.find('input', {'id': 'nombres'})['value'].strip()

        # Verificar que los datos se hayan obtenido correctamente
        if not (apellidop and apellidom and nombres):
            return False, "No se encontraron datos válidos para el DNI ingresado"

        nombre_lista_reniec = [apellidop, apellidom, nombres]
        print(f"Datos extraídos: {nombre_lista_reniec}")
        return True, nombre_lista_reniec

    except Exception as e:
        print(f"Error al validar DNI: {e}")
        return False, "Ocurrió un error al validar el DNI"

    finally:
        if driver:
            driver.quit()





@login_required
def perfil_usuario(request, user_id):
    usuario = request.user  # Obtienes el usuario autenticado
    perfil_actual = get_object_or_404(MiPerfil, user=usuario)
    tipo_usuario_actual = perfil_actual.tipo_usuario
    
    # Obtén al usuario según el ID pasado
    usuario = get_object_or_404(User, id=user_id)

    # Obtén el perfil asociado a ese usuario
    perfil = get_object_or_404(MiPerfil, user=usuario)
    tipo_usuario = perfil.tipo_usuario.lower()
    

    # Verificar si el usuario autenticado es un supervisor
    if tipo_usuario_actual == "supervisor(a)":        
        if tipo_usuario == "alumno(a)":
            usuario = get_object_or_404(User, id=user_id)
            # Manejo para tipo alumno
            alumno = get_object_or_404(Alumno, user=usuario)
            return render(request, 'perfil_usuario.html', {
                'usuario': usuario,
                'tipo_usuario': tipo_usuario,
                'alumno': alumno,
                'nombre_carrera': alumno.nombre_carrera,  # Usa el campo directamente
            })
        elif tipo_usuario == "supervisor(a)":
            usuario = get_object_or_404(User, id=user_id)
            # Manejo para tipo alumno
            supervisor = get_object_or_404(Supervisor, user=usuario)
            return render(request, 'perfil_usuario.html', {
                'usuario': usuario,
                'tipo_usuario': tipo_usuario,
                'supervisor': supervisor,
            })
        elif tipo_usuario == "profesor(a)":
            # Obtener al profesor asociado con el usuario
            profesor = get_object_or_404(Profesor, user=usuario)

            # Obtener los nombres de los cursos que enseña el profesor
            nombre_cursos = [curso.nombre_curso for curso in profesor.cursos.all()]

            # Obtener las capacitaciones del profesor
            capacitaciones = profesor.capacitaciones.split(", ") if profesor.capacitaciones else []
            
            # Obtener las encuestas relacionadas con ese profesor
            encuestas = Encuesta.objects.filter(profesor=profesor)
            encuestas_procesadas = []
            suma_promedios = 0
            total_encuestas = len(encuestas)
            
            # Obtener los reportes de clase asociados al profesor
            reportes_clase = profesor.reportes_clase.all().order_by('-fecha_creacion')
            rutas_reportes_clase = [reporte.archivo_pdf.url for reporte in reportes_clase]

            # Obtener los reportes de docente asociados al profesor
            reportes_docente = profesor.reportes.all().order_by('-fecha_creacion')
            rutas_reportes_docente = [reporte.archivo_pdf.url for reporte in reportes_docente]
            
            # Inicializar retroalimentacion como una cadena vacía o el valor predeterminado que necesites
            retroalimentacion = None
            retroalimentacion = profesor.retroalimentacion
            
            
            if request.method == 'POST':
                print(f'prueba del POST')
                retroalimentacion = request.POST.get('retroalimentacion')
                print(f'Retroalimentacion: {retroalimentacion}')

                # Obtener al profesor asociado a este usuario
                profesor = get_object_or_404(Profesor, user=usuario)

                # Guardar la retroalimentación en la columna correspondiente de Profesor
                profesor.retroalimentacion = retroalimentacion
                
                # Guardar los cambios en la base de datos
                profesor.save()
            
            
            for encuesta in encuestas:
                respuestas = [encuesta.pregunta1, encuesta.pregunta2, encuesta.pregunta3, encuesta.pregunta4]
                # Calcular el promedio de las respuestas (excluyendo respuestas None)
                promedio = sum(respuesta for respuesta in respuestas if respuesta is not None) / len([respuesta for respuesta in respuestas if respuesta is not None])
                suma_promedios += promedio
                
                encuestas_procesadas.append({
                    'promedio': round(promedio, 1),
                    'comentario': encuesta.pregunta5,
                    'fecha_creacion': encuesta.fecha_creacion,
                })
                
            # Calcular el promedio general
            promedio_general = round(suma_promedios / total_encuestas, 1) if total_encuestas > 0 else 0

            return render(request, 'perfil_usuario.html', {
                'usuario': usuario,
                'tipo_usuario': tipo_usuario,
                'tipo_usuario_actual': tipo_usuario_actual,
                'profesor': profesor,
                'nombre_cursos': nombre_cursos,
                'encuestas': encuestas_procesadas,  # Pasamos las encuestas procesadas a la plantilla
                'capacitaciones': capacitaciones,  # Pasamos las capacitaciones a la plantilla
                'promedio_general': promedio_general,  # Pasamos el promedio general a la plantilla
                'reportes_docente': rutas_reportes_docente,
                'reportes_clase': rutas_reportes_clase,
                'retroalimentacion': retroalimentacion,
            })
    else:
        if tipo_usuario == "alumno(a)":
            usuario = get_object_or_404(User, id=user_id)
            # Manejo para tipo alumno
            alumno = get_object_or_404(Alumno, user=usuario)
            return render(request, 'perfil_usuario.html', {
                'usuario': usuario,
                'tipo_usuario': tipo_usuario,
                'alumno': alumno,
                'nombre_carrera': alumno.nombre_carrera,  # Usa el campo directamente
            })
        
        elif tipo_usuario == "profesor(a)":
            # Buscar el Profesor cuyo perfil estás viendo
            usuario = get_object_or_404(User, id=user_id)
            profesor = get_object_or_404(Profesor, user=usuario)
            # Obtener los cursos del Profesor
            nombre_cursos = [curso.nombre_curso for curso in profesor.cursos.all()]

            return render(request, 'perfil_usuario.html', {
                'usuario': usuario,
                'tipo_usuario': tipo_usuario,
                'profesor': profesor,
                'nombre_cursos': nombre_cursos,
            })

        elif tipo_usuario_actual == "no especificado":
            # Si el tipo de usuario es el valor por defecto
            return render(request, 'perfil_no_especificado.html', {
                'usuario': usuario,
                'mensaje': "Este perfil no tiene un tipo de usuario asignado.",
            })

        else:
            # Maneja cualquier tipo de usuario no reconocido
            raise Http404("Tipo de usuario no reconocido.")
    



@login_required
def perfil_usuario_actual(request):
    usuario = request.user
    perfil = get_object_or_404(MiPerfil, user=usuario)
    tipo_usuario = perfil.tipo_usuario
    
    form_data = {
        'numero_telefono': request.POST.get('numero_telefono', '').lower(),
        'descripcion': request.POST.get('descripcion', '').lower(),
    }

    numero_telefono = form_data['numero_telefono']
    descripcion = form_data['descripcion']

    if tipo_usuario == "alumno(a)":
        alumno = Alumno.objects.get(user=request.user)
        form = AlumnoForm(request.POST, instance=alumno) if request.method == 'POST' else AlumnoForm(instance=alumno)

        if form.is_valid() and request.method == 'POST':
            alumno = form.save()
            alumno.numero_telefono = numero_telefono
            alumno.descripcion = descripcion
            alumno.save()

        return render(request, 'perfil_usuario_actual.html', {
            'form': form,
            'tipo_usuario': tipo_usuario,
            'usuario': usuario
        })

    elif tipo_usuario == "profesor(a)":
        profesor, created = Profesor.objects.get_or_create(user=request.user)
        form = ProfesorForm(request.POST, instance=profesor) if request.method == 'POST' else ProfesorForm(instance=profesor)
        usuario = request.user
        perfil = get_object_or_404(Profesor, user=usuario)
        reportes_docente = ReporteDocente.objects.filter(profesor_id=perfil.id).order_by('-fecha_creacion')
        reportes_clase = ReporteClase.objects.filter(profesor_id=perfil.id).order_by('-fecha_creacion')
        retroalimentacion = profesor.retroalimentacion
        
        # Inicializamos 'capacitaciones' antes de cualquier condición
        capacitaciones = []

        if form.is_valid() and request.method == 'POST':
            profesor = form.save(commit=False)
            capacitaciones = request.POST.getlist('capacitaciones[]', [])
            profesor.capacitaciones = ", ".join(capacitaciones)
            profesor.save()

        encuestas_procesadas = []
        suma_promedios = 0
        encuestas = Encuesta.objects.filter(profesor=profesor)

        for encuesta in encuestas:
            respuestas = [encuesta.pregunta1, encuesta.pregunta2, encuesta.pregunta3, encuesta.pregunta4]
            promedio = sum(respuesta for respuesta in respuestas if respuesta is not None) / len(respuestas)
            suma_promedios += promedio
            encuestas_procesadas.append({
                'promedio': round(promedio, 1),
                'comentario': encuesta.pregunta5,
                'fecha_creacion': encuesta.fecha_creacion,
            })

        promedio_general = round(suma_promedios / len(encuestas), 1) if encuestas else 0

        return render(request, 'perfil_usuario_actual.html', {
            'form': form,
            'tipo_usuario': tipo_usuario,
            'usuario': usuario,
            'nombre_cursos': [curso.nombre_curso for curso in profesor.cursos.all()],
            'capacitaciones': capacitaciones,
            'encuestas': encuestas_procesadas,
            'promedio_general': promedio_general,
            'perfil': perfil,
            'pdf_reporte_url': perfil.pdf_reporte.url if perfil.pdf_reporte else None,
            'reportes_docente': reportes_docente,
            'reportes_clase': reportes_clase,
            'retroalimentacion': retroalimentacion,
        })

    elif tipo_usuario == "supervisor(a)":
        supervisor, created = Supervisor.objects.get_or_create(user=request.user)
        form = SupervisorForm(request.POST, instance=supervisor) if request.method == 'POST' else SupervisorForm(instance=supervisor)

        if form.is_valid() and request.method == 'POST':
            form.save()

        return render(request, 'perfil_usuario_actual.html', {
            'form': form,
            'tipo_usuario': tipo_usuario,
            'usuario': usuario,
        })

    else:
        return render(request, 'perfil_usuario_actual.html', {
            'usuario': usuario,
            'error': "Tipo de usuario no reconocido.",
        })