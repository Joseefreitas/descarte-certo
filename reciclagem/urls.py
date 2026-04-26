from django.urls import path
from . import views

urlpatterns = [
    path('', views.reciclagem, name='reciclagem'),
]