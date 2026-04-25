from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout


def cadastro(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        if User.objects.filter(username=username).exists():
            return render(request, 'cadastro.html', {'erro': 'Usuário já existe'})

        user = User.objects.create_user(
            username=username,
            email=email,
            password=senha
        )

        user.first_name = first_name
        user.last_name = last_name
        user.save()

        return redirect('/login/')

    return render(request, 'cadastro.html')

def login_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            auth_login(request, user)  # 🔥 ISSO GUARDA O LOGIN
            return redirect('/home/')
        else:
            return render(request, 'login.html', {'erro': 'Dados inválidos'})

    return render(request, 'login.html')

def logout_usuario(request):
    logout(request)
    return redirect('/login/')
# Create your views here.
