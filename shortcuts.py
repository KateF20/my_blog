from django.http import Http404

from blog.models import Post


def get_object_or_404(slug):
    try:
        post = Post.objects.get(slug=slug)

    except Post.DoesNotExist:
        raise Http404("No Post matches the given slug.")

    return post
