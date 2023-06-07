from django.test import TestCase

from blog.models import Post


class GetPost(TestCase):
    fixtures = ['post.json', 'author.json', 'tags.json']

    def test_existing_post(self):
        post = Post.objects.get(pk=1)
        self.assertEqual(post.title, 'Gorge Hiking')

    def test_existing_author(self):
        post = Post.objects.get(pk=1)
        self.assertEqual(post.author.full_name, 'Kate Fed')

    def test_existing_tags(self):
        post = Post.objects.get(pk=1)
        tags = post.tags.values_list('pk', flat=True)
        self.assertIn(1, tags)


'''import pytest
from django.http.response import Http404

from blog.models import Post

from shortcuts import get_object_or_404



@pytest.mark.parametrize('kwargs, exc', [
    ({'slug': 'slug'}, Http404),
    ({}, Http404),
    ({'author_rating': 5}, AttributeError),
])
def test_404_failed(db, exc, kwargs):
    with pytest.raises(exc):
        get_object_or_404(model, **kwargs)


@pytest.mark.parametrize('kwargs, post_id', [
    ({'slug': 'slug'}, 1),
    ({}, 2),
    ({'author_rating': 5}, 3),
])
def test_404_ok(db, post_id, kwargs):
    post = get_object_or_404(model, **kwargs)
    assert post.id == post_id'''
