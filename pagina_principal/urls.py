from django.urls import path
from .views import *

urlpatterns = [
    path('', pagina_principal, name='pagina_principal'),  # Vista para app1
]