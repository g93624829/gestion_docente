from django.db import models
from autenticacion.models import Profesor

# Create your models here.
# Modelo para almacenar los reportes de clase
class ReporteClase(models.Model):
    profesor = models.ForeignKey(Profesor, related_name='reportes_clase', on_delete=models.CASCADE)
    archivo_pdf = models.FileField(upload_to='pdf_reportes_clase/')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reporte de {self.profesor.nombre_completo} - {self.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')}"
    
class ReporteDocente(models.Model):
    profesor = models.ForeignKey(Profesor, related_name='reportes', on_delete=models.CASCADE)
    archivo_pdf = models.FileField(upload_to='pdf_reportes_docente/')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reporte de {self.profesor.nombre_completo} - {self.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')}"