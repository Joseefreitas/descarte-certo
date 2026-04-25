"""
URL configuration for descarte_certo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from core import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # admin
    path('admin/', admin.site.urls),

    # login na página inicial
    path('', views.login_usuario, name='login'),

    # cadastro
    path('cadastro/', views.cadastro, name='cadastro'),

    # página inicial depois do login
    path('home/', views.home, name='home'),

    # guia de descarte
    path('guia-descarte/', views.guia_descarte, name='guia_descarte'),

    # logout
    path('logout/', views.logout_usuario, name='logout'),

    # apps
    path('comunidade/', include('comunidade.urls')),
    path('mapa/', include('mapa.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# para conseguir o usuário dar post de midia 