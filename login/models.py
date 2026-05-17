from django.db import models
from django.contrib.auth.models import User


class PessoaFisica(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='pessoa_fisica')
    # on_delete=models.CASCADE - faz com que se deletar o usuário tudo vinculador a ele vai ser apagado junto 
    cpf = models.CharField(max_length=14, unique=True)  # formato: 000.000.000-00
    # unique=True impede cadastro de cpf´s duplicados 

    def __str__(self):
        return f'{self.user.get_full_name()} - {self.cpf}'
        # vincula cada objeto usuário à um cpf 


class PessoaJuridica(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='pessoa_juridica')
        # on_delete=models.CASCADE - faz com que se deletar o usuário tudo vinculador a ele vai ser apagado junto 
    cnpj = models.CharField(max_length=18, unique=True)  # formato: 00.000.000/0000-00
        # unique=True impede cadastro de cnpj´s duplicados 
    razao_social = models.CharField(max_length=255)
    nome_fantasia = models.CharField(max_length=255, blank=True)
    
    bairros_atendidos = models.CharField(max_length=500, blank=True, help_text="Separe os bairros por vírgula. Ex: Boa Viagem, Recife, Afogados")
    tipos_residuo = models.CharField(max_length=255, blank=True, help_text="Separe por vírgula. Ex: papel, plastico, vidro")

    def __str__(self):
        return f'{self.razao_social} - {self.cnpj}'
            # vincula cada objeto usuário à um cnpj

    