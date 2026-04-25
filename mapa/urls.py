from django.urls import path
from . import views

app_name = 'mapa'

urlpatterns = [
    path('', views.mapa_view, name='index'),
    path('adicionar/', views.adicionar_ponto_view, name='adicionar'),
]