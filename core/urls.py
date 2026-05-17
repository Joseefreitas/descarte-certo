from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.shortcuts import redirect
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('/login/')),

    path('', include('login.urls')),
    path('', include('core.urls')),

    path('comunidade/', include('comunidade.urls')),
    path('mapa/', include('mapa.urls')),
    path('reciclagem/', include('reciclagem.urls')),
    path('coleta/', include('coleta.urls')),
    path('agendamento/', include('agendamento.urls')),

    path('accounts/login/', lambda request: redirect('/login/')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]