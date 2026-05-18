from django.contrib import admin
from .models import PessoaFisica, PessoaJuridica

admin.site.register(PessoaFisica)
admin.site.register(PessoaJuridica)