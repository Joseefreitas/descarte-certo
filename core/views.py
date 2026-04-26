from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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