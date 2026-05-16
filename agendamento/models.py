from django.db import models
from django.contrib.auth.models import User
from mapa.models import PontoColeta

TIPOS_RESIDUO = [
    ('papel', 'Papel e papelão'),
    ('plastico', 'Plástico'),
    ('organico', 'Orgânico'),
    ('eletronico', 'Eletrônico'),
    ('metais', 'Metais'),
    ('vidro', 'Vidro'),
]

TURNOS = [
    ('manha', 'Manhã (06h - 12h)'),
    ('tarde', 'Tarde (12h - 18h)'),
    ('noite', 'Noite (18h - 22h)'),
]

class Agendamento(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='agendamentos')
    ponto_coleta = models.ForeignKey(PontoColeta, on_delete=models.CASCADE, related_name='agendamentos')
    data = models.DateField()
    horario = models.TimeField(max_length=10, choices=TURNOS)
    tipo_residuo = models.CharField(max_length=50, choices=TIPOS_RESIDUO)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.ponto_coleta.nome} - {self.data}"