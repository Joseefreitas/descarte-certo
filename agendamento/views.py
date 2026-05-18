from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Agendamento
from login.models import PessoaJuridica

def buscar_empresa(bairro, tipo_residuo):
    empresas = PessoaJuridica.objects.all()
    for empresa in empresas:
        bairros = [b.strip().lower() for b in empresa.bairros_atendidos.split(',')]
        tipos = [t.strip().lower() for t in empresa.tipos_residuo.split(',')]
        if bairro.lower() in bairros and tipo_residuo.lower() in tipos:
            return empresa
    return None

@login_required(login_url='/login/')
def criar_agendamento(request):
    agendamentos = Agendamento.objects.filter(usuario=request.user).order_by('-data')

    if request.method == 'POST':
        bairro = request.POST.get('bairro')
        data = request.POST.get('data')
        horario = request.POST.get('horario')
        tipo_residuo = request.POST.get('tipo_residuo')

        empresa = buscar_empresa(bairro, tipo_residuo)

        if not empresa:
            messages.error(request, 'Nenhuma empresa disponível para esse bairro e tipo de resíduo.')
            return redirect('criar_agendamento')

        Agendamento.objects.create(
            usuario=request.user,
            empresa=empresa,
            bairro=bairro,
            data=data,
            horario=horario,
            tipo_residuo=tipo_residuo,
        )
        messages.success(request, 'Agendamento realizado com sucesso!')
        return redirect('criar_agendamento')

    return render(request, 'agendamento.html', {'agendamentos': agendamentos})