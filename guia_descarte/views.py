from django.shortcuts import render

from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def guia_descarte(request):
    return render(request, 'guia_descarte.html')

# Create your views here.
def guia_descarte(request):
    return render(request, 'guia_descarte.html')
