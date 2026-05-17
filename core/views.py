from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

# ======================
# HOME
# ======================
def home(request):
    modo_visitante = request.session.get('modo_visitante', False)
    return render(request, 'index.html', {
        'modo_visitante': modo_visitante
    })

# ======================
# GUIA DE DESCARTE (protegida)
# ======================
@login_required(login_url='/login/')
def guia_descarte(request):
    return render(request, 'guia_descarte.html')

# ======================
# MODO VISITANTE
# ======================
def modo_visitante(request):
    request.session['modo_visitante'] = True
    return redirect('home')

# ======================
# LOGOUT
# ======================
def logout_usuario(request):
    logout(request)
    return redirect('login')