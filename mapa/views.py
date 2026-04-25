from django.shortcuts import render
from .models import PontoColeta

from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def mapa(request):
    return render(request, 'mapa.html')

# Create your views here.
def mapa_view(request):
    pontos_no_banco = PontoColeta.objects.all() 
    return render(request, 'mapa.html', {'pontos': pontos_no_banco})
