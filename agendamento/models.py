from django.db import models
from django.contrib.auth.models import User
from mapa.models import PontoColeta

TIPOS_RESIDUO = [
    ('domiciliar', 'Domiciliar'),
    ('reciclavel', 'Reciclável'),
    ('organico', 'Orgânico'),
    ('eletronico', 'Eletrônico'),
    ('volumoso', 'Volumoso'),
]

class Agendamento(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='agendamentos')
    ponto_coleta = models.ForeignKey(PontoColeta, on_delete=models.CASCADE, related_name='agendamentos')
    data = models.DateField()
    horario = models.TimeField()
    tipo_residuo = models.CharField(max_length=50, choices=TIPOS_RESIDUO)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.ponto_coleta.nome} - {self.data}"