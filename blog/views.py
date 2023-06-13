from django.shortcuts import render, get_object_or_404

from .models import Post, Author, Tag
from shortcuts import get_object_or_404


def index(request):
    latest_posts = Post.objects.all().order_by('-date')[:3]
    context = {
        'latest_posts': latest_posts
    }
    return render(request, 'blog/index.html', context)


def posts(request):
    all_posts = Post.objects.all().order_by('-date')
    context = {
        'all_posts': all_posts
    }
    return render(request, 'blog/all_posts.html', context)


def single_post(request, slug, name):
    post = get_object_or_404(Post, slug=slug, name=name)
    context = {
        'post': post,
        'tags': post.tags.all()
    }
    return render(request, 'blog/single_post.html', context)
