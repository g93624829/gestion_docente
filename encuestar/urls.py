from django.urls import path
from .views import (
    encuestar,
)

urlpatterns = [
    path('', encuestar, name='encuestar'),
]