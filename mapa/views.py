from django.shortcuts import render, redirect
from .models import PontoColeta
from django.contrib import messages

def mapa_view(request):
    pontos = PontoColeta.objects.all()
    return render(request, 'mapa.html', {'pontos': pontos})

def adicionar_ponto_view(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        endereco = request.POST.get('endereco')
        tipo_residuo = request.POST.get('tipo_residuo')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        if nome and endereco and latitude and longitude:
            try:
                PontoColeta.objects.create(
                    nome=nome,
                    endereco=endereco,
                    tipo_residuo=tipo_residuo,
                    latitude=float(latitude.replace(',', '.')),
                    longitude=float(longitude.replace(',', '.'))
                )
                messages.success(request, "Ponto adicionado com sucesso!")
                return redirect('mapa:index')
            except Exception as e:
                return render(request, 'adicionar_ponto.html', {'erro': f'Erro: {e}'})
    
    return render(request, 'adicionar_ponto.html')