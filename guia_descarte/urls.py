from django.urls import path
from . import views

urlpatterns = [
    path('', views.guia_descarte, name='guia_descarte'),
 
]