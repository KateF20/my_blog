from django.http import Http404

from blog.models import Post


def get_post_by_slug(slug):
    try:
        post = Post.objects.get(slug=slug)

    except Post.DoesNotExist:
        raise Http404("No Post matches the given slug.")

    return post
