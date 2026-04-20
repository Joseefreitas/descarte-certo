from django.shortcuts import render, redirect
from .models import Topic, Post

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

def topic_detail(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if request.method == 'POST':
        conteudo = request.POST.get('conteudo')

        if request.user.is_authenticated:
            autor = request.user

        else: 
            autor = None
        
        Post.objects.create(
            topic=topic,
            content=conteudo,
            author=autor
        )
    posts = topic.posts.all().order_by('created_at')

    return render(request, 'topic_detail.html',{
        'topic' : topic,
        'posts' : posts
    } 
    )