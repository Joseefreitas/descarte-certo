from django.db import models
from django.contrib.auth.models import User

#posts
class Topic(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    imagem = models.ImageField(upload_to='comunidade/', blank=True, null=True)  # ← novo
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

#respostas
class Post(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resposta em {self.topic.title}"
