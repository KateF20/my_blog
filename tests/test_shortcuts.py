import pytest
from django.http.response import Http404
from django.core.exceptions import FieldError

from shortcuts import get_object_or_404

from tests.models import MyModel


@pytest.mark.parametrize('kwargs, exc', [
    ({'slug': 'slug'}, Http404),
    ({}, Http404),
    ({'author_rating': 5}, FieldError),
])
def test_404_failed(db, exc, kwargs):
    with pytest.raises(exc):
        get_object_or_404(MyModel, **kwargs)


@pytest.fixture
def my_model(db):
    return MyModel.objects.create(slug='slug')


@pytest.mark.parametrize('kwargs, post_id', [
    ({'slug': 'slug'}, 1),
])
def test_404_ok(my_model, post_id, kwargs):
    post = get_object_or_404(MyModel, **kwargs)
    assert post.id == post_id
