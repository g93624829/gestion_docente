from django.db import models
from autenticacion.models import Alumno, Profesor  # Importamos los modelos de la app autenticacion

class Encuesta(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)  # Relacionamos con el modelo Alumno
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)  # Relacionamos con el modelo Profesor
    
    # Preguntas de la encuesta
    pregunta1 = models.PositiveSmallIntegerField()
    pregunta2 = models.PositiveSmallIntegerField()
    pregunta3 = models.PositiveSmallIntegerField()
    pregunta4 = models.PositiveSmallIntegerField()
    pregunta5 = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Fecha de creación

    class Meta:
        unique_together = ('alumno', 'profesor')  # Aseguramos que un alumno no pueda encuestar al mismo profesor más de una vez

    def __str__(self):
        return f"Encuesta de {self.alumno.user.username} a {self.profesor.user.username}"