from django.shortcuts import render

from django.contrib.auth.decorators import login_required

# Create your views here.
def guia_descarte(request):
    return render(request, 'guia_descarte.html')
