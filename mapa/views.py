from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import PontoColeta
from django.contrib import messages

def mapa_view(request):
    pontos = PontoColeta.objects.all()
    return render(request, 'mapa.html', {'pontos': pontos})

@login_required
def adicionar_ponto_view(request):
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        endereco = request.POST.get('endereco', '').strip()
        tipo_residuo = request.POST.get('tipo_residuo', '').strip()
        lat_raw = request.POST.get('latitude', '').replace(',', '.')
        lng_raw = request.POST.get('longitude', '').replace(',', '.')

        if not all([nome, endereco, lat_raw, lng_raw]):
            messages.error(request, "Todos os campos obrigatórios devem ser preenchidos.")
            return render(request, 'adicionar_ponto.html')

        try:
            latitude = float(lat_raw)
            longitude = float(lng_raw)
        except ValueError:
            messages.error(request, "Coordenadas geográficas inválidas. Use apenas números.")
            return render(request, 'adicionar_ponto.html')

        try:
            PontoColeta.objects.create(
                nome=nome,
                endereco=endereco,
                tipo_residuo=tipo_residuo,
                latitude=latitude,
                longitude=longitude
            )
            messages.success(request, "Ponto de coleta cadastrado com sucesso!")
            return redirect('mapa:index')
        except Exception as e:
            messages.error(request, f"Erro interno ao salvar no banco: {e}")
            return render(request, 'adicionar_ponto.html')

    return render(request, 'adicionar_ponto.html')