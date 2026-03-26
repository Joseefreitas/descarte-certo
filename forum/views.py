from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def ver_forum(request):
    return render(request,  'ver_forum.html')