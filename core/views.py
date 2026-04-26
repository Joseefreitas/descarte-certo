from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# ======================
# HOME (protegida)
# ======================
def home(request):
    modo_visitante = request.session.get('modo_visitante', False)

    return render(request, 'index.html', {
        'modo_visitante': modo_visitante
    })

def modo_visitante(request):
    request.session['modo_visitante'] = True
    return redirect('home')

# ======================
# GUIA DE DESCARTE (protegida)
# ======================
@login_required(login_url='/login/')
def guia_descarte(request):
    return render(request, 'guia_descarte.html')


# ======================
# CADASTRO
# ======================
def cadastro(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        if User.objects.filter(username=username).exists():
            return render(request, 'cadastro.html', {
                'erro': 'Esse usuário já existe.'
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=senha
        )

        user.first_name = first_name
        user.last_name = last_name
        user.save()

        return redirect('login')

    return render(request, 'cadastro.html')


# ======================
# LOGIN
# ======================
def login_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')  # ⚠️ TEM QUE SER "password"

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')

        return render(request, 'login.html', {
            'erro': 'Usuário ou senha inválidos.'
        })

    return render(request, 'login.html')


# ======================
# LOGOUT
# ======================
def logout_usuario(request):
    logout(request)
    return redirect('login')