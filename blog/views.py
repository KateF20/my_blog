from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views.generic import ListView
from django.views import View

from .models import Post, Author, Tag
from .forms import CommentForm


class IndexView(ListView):
    template_name = 'blog/index.html'
    model = Post
    ordering = ['-date']
    context_object_name = 'posts'

    def get_queryset(self):
        query_set = super().get_queryset()
        data = query_set[:3]
        return data


class AllPostsView(ListView):
    template_name = 'blog/all_posts.html'
    model = Post
    ordering = ['-date']
    context_object_name = 'all_posts'


class SinglePostView(View):
    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        context = {
            'post': post,
            'post_tags': post.tags.all(),
            'comment_form': CommentForm(),
            'comments': post.comments.all().order_by('-id')
        }
        return render(request, 'blog/single_post.html', context)

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()

            return HttpResponseRedirect(reverse('single-post', args=[slug]))

        context = {
            'post': post,
            'post_tags': post.tags.all(),
            'comment_form': comment_form,
            'comments': post.comments.all().order_by('-id')

        }

        return render(request, 'blog/single_post.html', context)

