from django.shortcuts import render

@login_required(login_url='/login/')
def guia_descarte(request):
    return render(request, 'guia_descarte.html')

# Create your views here.
def guia_descarte(request):
    return render(request, 'guia_descarte.html')
