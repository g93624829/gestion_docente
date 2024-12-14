from django.contrib.auth.models import User
from django.db import models
    
class Carrera(models.Model):
    codigo_carrera = models.CharField(max_length=10, unique=True)  # Código único para el curso
    nombre_carrera = models.CharField(max_length=255)  # Nombre del curso
    
    def __str__(self):
        return f"{self.codigo_carrera} - {self.nombre_carrera}"


class Curso(models.Model):
    codigo_curso = models.CharField(max_length=10, unique=True)  # Código único para el curso
    nombre_curso = models.CharField(max_length=255)  # Nombre del curso

    def __str__(self):
        return f"{self.codigo_curso} - {self.nombre_curso}"

class MiPerfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_mi')
    dni = models.CharField(max_length=8, unique=True)
    tipo_usuario = models.CharField(max_length=50, default='no especificado')
    nombre_usuario = models.CharField(max_length=200, default='no especificado')  # Este es independiente de `username` en User
    correo_electronico = models.CharField(max_length=200, default='no especificado')  # Este es independiente de `email` en User
    descripcion = models.TextField(blank=True, null=True)
    numero_telefono = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.tipo_usuario}"
    
    
    
class Alumno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_alumno')
    dni = models.CharField(max_length=8, unique=True)
    correo_electronico = models.CharField(max_length=200, default='no especificado')
    nombre_completo = models.CharField(max_length=200, default='no especificado')
    nombre_carrera = models.CharField(max_length=255, blank=True, null=True)
    nombres = models.CharField(max_length=200, default='no especificado')
    apellido_paterno = models.CharField(max_length=200, default='no especificado')
    apellido_materno = models.CharField(max_length=200, default='no especificado')
    numero_telefono = models.CharField(max_length=15, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    codigo_carrera = models.CharField(max_length=10, blank=True, null=True)  # Nuevo campo
    tipo_usuario = models.CharField(max_length=50, default='no especificado')

    def save(self, *args, **kwargs):
        # Rellenar los campos de código y nombre de la carrera automáticamente
        if self.carrera:
            self.codigo_carrera = self.carrera.codigo_carrera
            self.nombre_carrera = self.carrera.nombre_carrera
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.tipo_usuario} - {self.carrera}"
    

class Profesor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_profesor')
    dni = models.CharField(max_length=8, unique=True)
    correo_electronico = models.CharField(max_length=200, default='no especificado')
    nombre_completo = models.CharField(max_length=200, default='no especificado')
    nombres = models.CharField(max_length=200, default='no especificado')
    apellido_paterno = models.CharField(max_length=200, default='no especificado')
    apellido_materno = models.CharField(max_length=200, default='no especificado')
    numero_telefono = models.CharField(max_length=9, blank=True, null=True)
    capacitaciones = models.TextField(blank=True, null=True, default='No hay capacitaciones')
    descripcion = models.TextField(blank=True, null=True)
    retroalimentacion = models.TextField(blank=True, null=True, default='Agregar retroalimentación')
    cursos = models.ManyToManyField(Curso, related_name='profesores')  # Relación con cursos
    tipo_usuario = models.CharField(max_length=50, default='profesor(a)')
    # Nuevo campo para guardar el PDF
    pdf_reporte = models.FileField(upload_to='pdf_reports/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.tipo_usuario}"


class Supervisor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_supervisor')
    dni = models.CharField(max_length=8, unique=True)
    correo_electronico = models.CharField(max_length=200, default='no especificado')
    nombre_completo = models.CharField(max_length=200, default='no especificado')
    nombres = models.CharField(max_length=200, default='no especificado')
    apellido_paterno = models.CharField(max_length=200, default='no especificado')
    apellido_materno = models.CharField(max_length=200, default='no especificado')
    numero_telefono = models.CharField(max_length=9, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    tipo_usuario = models.CharField(max_length=50, default='supervisor(a)')

    def __str__(self):
        return f"{self.user.username} - {self.tipo_usuario}"