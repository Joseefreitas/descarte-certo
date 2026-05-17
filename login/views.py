from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from .models import PessoaFisica, PessoaJuridica


def eusou(request):
    return render(request, 'eusou.html')


def cadastropessoafisica(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        cpf = request.POST.get('cpf')

        if User.objects.filter(username=username).exists():
            return render(request, 'cadastropessoafisica.html', {'erro': 'Usuário já existe'})

        user = User.objects.create_user(username=username, email=email, password=senha)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        PessoaFisica.objects.create(user=user, cpf=cpf)

        return redirect('/login/')

    return render(request, 'cadastropessoafisica.html')


def cadastropessoajuridica(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        cnpj = request.POST.get('cnpj')
        razao_social = request.POST.get('razao_social')
        nome_fantasia = request.POST.get('nome_fantasia')
        bairros_atendidos = request.POST.get('bairros_atendidos')
        tipos_residuo = request.POST.getlist('tipos_residuo')

        if User.objects.filter(username=username).exists():
            return render(request, 'cadastropessoajuridica.html', {'erro': 'Usuário já existe'})

        user = User.objects.create_user(username=username, email=email, password=senha)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        PessoaJuridica.objects.create(user=user, cnpj=cnpj, razao_social=razao_social, nome_fantasia=nome_fantasia,  bairros_atendidos=bairros_atendidos,  tipos_residuo=','.join(tipos_residuo),)

        return redirect('/login/')

    return render(request, 'cadastropessoajuridica.html')


def login_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            auth_login(request, user)
            return redirect('/home/')
        else:
            return render(request, 'login.html', {'erro': 'Dados inválidos'})

    return render(request, 'login.html')


def logout_usuario(request):
    logout(request)
    return redirect('/login/')