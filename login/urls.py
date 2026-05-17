from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
    path('cadastro/', views.eusou, name='eusou'),
    path('cadastro/cadastropessoafisica/', views.cadastropessoafisica, name='cadastropessoafisica'),
    path('cadastro/cadastropessoajuridica/', views.cadastropessoajuridica, name='cadastropessoajuridica'),
]