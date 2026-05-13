from django.urls import path
from . import views

urlpatterns = [
    path('agenda/', views.buscar_agenda, name='buscar_agenda'),
]