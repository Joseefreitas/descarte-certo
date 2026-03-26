from django.urls import path
from . import views

urlpatterns = [
    path('ver_forum/', views.ver_forum, name="ver_forum")

]
