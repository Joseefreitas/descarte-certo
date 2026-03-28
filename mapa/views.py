from django.shortcuts import render
from .models import PontoColeta

# Create your views here.
def mapa_view(request):
    pontos_no_banco = PontoColeta.objects.all() 
    return render(request, 'mapa.html', {'pontos': pontos_no_banco})
