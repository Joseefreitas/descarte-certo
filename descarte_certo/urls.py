from django.contrib import admin
from django.urls import path, include, re_path
from core import views
from django.conf import settings
from django.views.static import serve
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),

    # Login/cadastro primeiro — para os names serem registrados sem conflito
    path('', include('login.urls')),

    # Core
    path('logout/', views.logout_usuario, name='logout'),
    path('guest/', views.modo_visitante, name='guest'),
    path('home/', views.home, name='home'),
    path('guia-descarte/', views.guia_descarte, name='guia_descarte'),

    # Apps
    path('comunidade/', include('comunidade.urls')),
    path('mapa/', include('mapa.urls')),
    path('reciclagem/', include('reciclagem.urls')),
    path('coleta/', include('coleta.urls')),
    path('agendamento/', include('agendamento.urls')),

    path('accounts/login/', lambda request: redirect('/login/')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

    # Redireciona raiz para login (por último, para não engolir outras rotas)
    path('', lambda request: redirect('/login/')),
]