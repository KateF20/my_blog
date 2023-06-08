import pytest
from django.test import TestCase

from blog.models import Post


@pytest.fixture()
def connection():
    return 'connection'


class GetPost(TestCase):
    fixtures = ['tests/fixtures/post.json', 'tests/fixtures/author.json', 'tests/fixtures/tags.json']

    def test_existing_post(self, connection):
        post = Post.objects.get(pk=1)
        assert post.title == 'Gorge Hiking'
        assert connection == 'connection'

    def test_existing_author(self):
        post = Post.objects.get(pk=1)
        self.assertEqual(post.author.full_name, 'Kate Fed')

    def test_existing_tags(self):
        post = Post.objects.get(pk=1)
        tags = post.tags.values_list('pk', flat=True)
        self.assertIn(1, tags)
