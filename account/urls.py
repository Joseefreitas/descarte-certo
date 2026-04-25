from django.urls import path
from . import views
urlpatterns = [
    path('', views.loguin, name='loguin'),
]