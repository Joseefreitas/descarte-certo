from django.shortcuts import render, get_object_or_404
from .models import Topic, Post

def comunidade(request):
    topics = Topic.objects.all().order_by('-created_at')
    return render(request, 'comunidade/comunidade.html', {'topics': topics})


def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    posts = topic.posts.all()

    return render(request, 'comunidade/topic_details.html', {
        'topic': topic,
        'posts': posts
    })