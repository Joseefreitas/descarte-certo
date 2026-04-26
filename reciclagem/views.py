from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def reciclagem(request):
    return render(request, 'reciclagem.html')

# Create your views here.
def reciclagem(request):
    return render(request, 'reciclagem.html')