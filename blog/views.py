from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views.generic import ListView, View

from .models import Post
from .forms import CommentForm
from detail_view_func import DetailView


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        read_later_posts = self.request.session.get('read_later_posts', [])
        context['is_saved'] = self.object.id in read_later_posts
        context['comments'] = self.object.comments.all().order_by('-id')
        context['tags'] = self.object.tags.all()
        context['comment_form'] = CommentForm()
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
        read_later_posts = request.session.get('read_later_posts')
        context = {}

        if read_later_posts is not None:
            posts = Post.objects.filter(id__in=read_later_posts)
        context['posts'] = posts

        return render(request, 'blog/read_later_posts.html', context)

    def post(self, request):
        read_later_posts = request.session.get('read_later_posts')
        post_id = int(request.POST['post_id'])

        if post_id in read_later_posts:
            read_later_posts.remove(post_id)
        else:
            read_later_posts.append(post_id)

        request.session['read_later_posts'] = read_later_posts
        request.session.modified = True

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
