from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Topic

@login_required(login_url='/login/')
def comunidade(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        conteudo = request.POST.get('conteudo')
        imagem = request.FILES.get('imagem')

        Topic.objects.create(
            title=titulo,
            content=conteudo,
            imagem=imagem,
            author=request.user
        )
        return redirect('comunidade')

    topics = Topic.objects.all().order_by('-created_at')
    
    for t in topics:
        print(f"topic: {t.title} | author_id: {t.author_id} | user_id: {request.user.id}")
    
    return render(request, 'comunidade.html', {'topics': topics})


def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    posts = topic.posts.all()

    if request.method == 'POST':
        conteudo = request.POST.get('conteudo')
        if request.user.is_authenticated:
            topic.posts.create(content=conteudo, author=request.user)
        return redirect('topic_detail', topic_id=topic_id)

    return render(request, 'topic_detail.html', {'topic': topic, 'posts': posts})


@login_required(login_url='/login/')
def deletar_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if request.user == topic.author:
        topic.delete()
        messages.error(request, 'Post apagado com sucesso!')
    return redirect('comunidade')