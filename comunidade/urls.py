from django.urls import path
from . import views

urlpatterns = [
    path('', views.comunidade, name='comunidade'),
    # para carregar foto 
    path('<int:topic_id>/', views.topic_detail, name='topic_detail'),
    # para conseguir o usuário apagar uma postagem que ele fez
 path('<int:topic_id>/deletar/', views.deletar_topic, name='deletar_topic'),
]