from django.urls import path
from . import views

urlpatterns = [
    path('', views.criar_agendamento, name='criar_agendamento'),
    path('meus/', views.meus_agendamentos, name='meus_agendamentos'),
]