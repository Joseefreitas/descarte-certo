from django.db import models

# Create your models here.
class PontoColeta(models.Model):
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=255)
    
    # Coordenadas exatas para o Leaflet achar no mapa
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    tipo_residuo = models.CharField(max_length=100) 

    def __str__(self):
        return self.nome
