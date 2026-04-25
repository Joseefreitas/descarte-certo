from django.shortcuts import render, redirect
from .models import Topic
from django.contrib.auth.decorators import login_required

def comunidade(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        conteudo = request.POST.get('conteudo')
        imagem = request.FILES.get('imagem')  # ← novo

        if request.user.is_authenticated:
            autor = request.user
        else:
            autor = None

        Topic.objects.create(
            title=titulo,
            content=conteudo,
            imagem=imagem,  # ← novo
            author=autor
        )

        return redirect('comunidade')

    topics = Topic.objects.all().order_by('-created_at')
    return render(request, 'comunidade.html', {'topics': topics})
def topic_detail(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    posts = topic.post_set.all()
    
    if request.method == 'POST':
        conteudo = request.POST.get('conteudo')
        if request.user.is_authenticated:
            autor = request.user
        else:
            autor = None
        topic.post_set.create(content=conteudo, author=autor)
        return redirect('topic_detail', topic_id=topic_id)
    
    return render(request, 'topic_detail.html', {'topic': topic, 'posts': posts})

@login_required
# função para o usuário conseguir deletar seu post
def deletar_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if request.user == topic.author:
        topic.delete()
    return redirect('comunidade')