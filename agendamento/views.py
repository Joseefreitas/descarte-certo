from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Agendamento
from mapa.models import PontoColeta

@login_required(login_url='/login/')
def criar_agendamento(request):
    pontos = PontoColeta.objects.all()

    if request.method == 'POST':
        ponto_id = request.POST.get('ponto_coleta')
        data = request.POST.get('data')
        horario = request.POST.get('horario')
        tipo_residuo = request.POST.get('tipo_residuo')

        try:
            ponto = PontoColeta.objects.get(id=ponto_id)
            Agendamento.objects.create(
                usuario=request.user,
                ponto_coleta=ponto,
                data=data,
                horario=horario,
                tipo_residuo=tipo_residuo,
            )
            messages.success(request, 'Agendamento realizado com sucesso!')
            return redirect('meus_agendamentos')
        except PontoColeta.DoesNotExist:
            messages.error(request, 'Ponto de coleta inválido.')

    return render(request, 'agendamento.html', {'pontos': pontos})

@login_required(login_url='/login/')
def meus_agendamentos(request):
    agendamentos = Agendamento.objects.filter(usuario=request.user).order_by('-data')
    return render(request, 'agendamento.html', {'agendamentos': agendamentos})