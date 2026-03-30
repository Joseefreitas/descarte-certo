from django.shortcuts import render

# Create your views here.
def guia_descarte(request):
    return render(request, 'guia_descarte.html')
