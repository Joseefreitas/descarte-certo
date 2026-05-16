from django.urls import path
from . import views

urlpatterns = [
    path('', views.criar_agendamento, name='criar_agendamento'),
]