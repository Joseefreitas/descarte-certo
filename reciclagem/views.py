from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# @login_required(login_url='/login/')
# a tag loguin_required serve para dizer que só usa essa função quem tem
def reciclagem(request):
    return render(request, 'reciclagem.html')
