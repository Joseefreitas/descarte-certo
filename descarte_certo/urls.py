from django.contrib import admin
from django.urls import path, include, re_path
from core import views
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.views.static import serve
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('/login/')), 
    path('logout/', views.logout_usuario, name='logout'),
    path('guest/', views.modo_visitante, name='guest'),
    path('home/', views.home, name='home'),

    path('comunidade/', include('comunidade.urls')),
    path('mapa/', include('mapa.urls')),
    path('guia-descarte/', views.guia_descarte, name='guia_descarte'),
    path('reciclagem/', include('reciclagem.urls')),

    path('accounts/login/', lambda request: redirect('/login/')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

    path('coleta/', include('coleta.urls')),
    path('agendamento/', include('agendamento.urls')),

    path('', include('login.urls')),  # login, cadastro, eusou aqui
]