from django.shortcuts import render, redirect
from .models import Topic

def comunidade(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        conteudo = request.POST.get('conteudo')

      
        if request.user.is_authenticated:
            autor = request.user
        else:
            autor = None

        Topic.objects.create(
            title=titulo,
            content=conteudo,
            author=autor
        )

        return redirect('comunidade')

    topics = Topic.objects.all().order_by('-created_at')

    return render(request, 'comunidade.html', {'topics': topics})