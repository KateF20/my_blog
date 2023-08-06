from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView, View

from .models import Post
from .forms import CommentForm
from detail_view_func import DetailView
from shortcuts import get_object_or_404


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


class SinglePostView(DetailView):
    template_name = 'blog/single_post.html'
    model = Post
    context_object_name = 'post'

    def get_context_data(self, object, comment_form=None, **kwargs):
        context = super().get_context_data(object=object, **kwargs)
        read_later_posts = self.request.session.get('read_later_posts', [])
        context['is_saved'] = object.id in read_later_posts
        context['comments'] = object.comments.all().order_by('-id')
        context['tags'] = object.tags.all()
        context['comment_form'] = comment_form or CommentForm()
        return context

    def post(self, request, slug):
        post = self.object = self.get_object()
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse('single-post', args=[slug]))

        context = self.get_context_data(object=post, comment_form=comment_form)
        return self.render_to_response(context)


class ReadLaterView(View):
    def get(self, request):
        read_later_posts = request.session.get('read_later_posts', [])
        context = {}

        if read_later_posts is not None:
            context['posts'] = Post.objects.filter(id__in=read_later_posts)

        return render(request, 'blog/read_later_posts.html', context)

    def post(self, request):
        read_later_posts = request.session.get('read_later_posts', [])
        post_id = int(request.POST['post_id'])
        action = request.POST.get('action')
        slug = get_object_or_404(Post, pk=post_id).slug

        if action == 'remove':
            if post_id in read_later_posts:
                read_later_posts.remove(post_id)
        else:
            if post_id not in read_later_posts:
                read_later_posts.append(post_id)

        request.session['read_later_posts'] = read_later_posts

        return redirect('single-post', slug=slug)
