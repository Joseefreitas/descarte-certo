from django.urls import path
from . import views

urlpatterns = [
    path('', views.comunidade, name='comunidade'),
    path('<int:topic_id>/', views.topic_detail, name='topic_detail'),
    path('<int:topic_id>/deletar/', views.deletar_topic, name='deletar_topic'),
]