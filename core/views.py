from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

#pagina principal
@login_required
def home(request):
    return render(request, 'index.html')

def guia_descarte(request):
    return render(request, 'guia_descarte.html')

#cadastro
def cadastro(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        if User.objects.filter(username=username).exists():
            return render(request, 'cadastro.html' , {
                'erro': 'Esse usuário já existe.'
            })
        
        User.objects.create_user(
            username=username,
            email=email,
            password=senha
        )
        return redirect('login')
    return render(request, 'cadastro.html')

#login
def login_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = authenticate(
            request,
            username=username,
            password=senha
        )

        if user is not None:
            login(request, user)
            return redirect('home')

        return render(request, 'login.html', {
            'erro': 'Usuário ou senha inválidos.'
        })

    return render(request, 'login.html')

#logout
def logout_usuario(request):
    logout(request)
    return redirect('login')