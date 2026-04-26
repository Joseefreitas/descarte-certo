from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_usuario, name='login'),
    path('login/', views.login_usuario, name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('home/', views.home, name='home'),
    path('guia-descarte/', views.guia_descarte, name='guia_descarte'),
    path('logout/', views.logout_usuario, name='logout'),
    path('guest/', views.modo_visitante, name='guest')
]