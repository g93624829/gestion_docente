from django import forms
from .models import *

class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = [
            'numero_telefono',
            'descripcion',
        ]
        widgets = {
            'numero_telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su número de teléfono'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingrese una breve descripción', 'rows': 3}),
        }


class ProfesorForm(forms.ModelForm):
    class Meta:
        model = Profesor
        fields = [
            'numero_telefono',
            'descripcion',
            'capacitaciones',
        ]
        widgets = {
            'numero_telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su número de teléfono'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Como se describe usted', 'rows': 3}),
            'capacitaciones': forms.HiddenInput(),  # Oculto porque lo gestionas con JavaScript
        }
        

class SupervisorForm(forms.ModelForm):
    class Meta:
        model = Supervisor
        fields = [
            'numero_telefono',
            'descripcion',
        ]
        widgets = {
            'numero_telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su número de teléfono'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Como se describe usted', 'rows': 3}),
        }