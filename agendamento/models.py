from django.db import models
from django.contrib.auth.models import User
from login.models import PessoaJuridica

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
    empresa = models.ForeignKey(PessoaJuridica, on_delete=models.SET_NULL, null=True, blank=True, related_name='agendamentos')
    bairro = models.CharField(max_length=100)
    data = models.DateField()
    horario = models.CharField(max_length=10, choices=TURNOS)
    tipo_residuo = models.CharField(max_length=50, choices=TIPOS_RESIDUO)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.ponto_coleta.nome} - {self.data}"