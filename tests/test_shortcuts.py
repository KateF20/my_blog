from blog.models import Post

from shortcuts import get_object_or_404


def test_sum():
    post = get_object_or_404(Post, slug='slug')
    assert post.slug == 'slug'
