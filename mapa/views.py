from django.shortcuts import render, redirect
from .models import PontoColeta

from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def mapa(request):
    return render(request, 'mapa.html')

# Create your views here.
def mapa_view(request):
    pontos_no_banco = PontoColeta.objects.all()
    return render(request, 'mapa.html', {'pontos': pontos_no_banco})

def adicionar_ponto_view(request):
    erro = None
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        endereco = request.POST.get('endereco', '').strip()
        tipo_residuo = request.POST.get('tipo_residuo', '').strip()
        latitude = request.POST.get('latitude', '').strip()
        longitude = request.POST.get('longitude', '').strip()

        if not all([nome, endereco, tipo_residuo, latitude, longitude]):
            erro = 'Todos os campos são obrigatórios.'
        else:
            try:
                PontoColeta.objects.create(
                    nome=nome,
                    endereco=endereco,
                    tipo_residuo=tipo_residuo,
                    latitude=float(latitude.replace(',', '.')),
                    longitude=float(longitude.replace(',', '.')),
                )
                return redirect('mapa:index')
            except ValueError:
                erro = 'Latitude e longitude devem ser números válidos.'

    return render(request, 'adicionar_ponto.html', {'erro': erro})