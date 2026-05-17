from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.eusou, name='eusou'),
    #path('cadastro/empresa/', views.cadastro_empresa, name='cadastro_empresa'),
    #path('cadastro/pessoa-fisica/', views.cadastro_pessoa_fisica, name='cadastro_pessoa_fisica'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
]