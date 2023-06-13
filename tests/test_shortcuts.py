import pytest
from django.contrib.auth import get_user_model
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
def my_user(db):
    User = get_user_model()
    return User.objects.create()


@pytest.fixture
def my_model(db, my_user):
    return MyModel.objects.create(slug='slug', user=my_user)


@pytest.mark.parametrize('objects, kwargs, post_id', [
    (MyModel, {'slug': 'slug'}, 1),
    (MyModel.objects.filter(user_id=1), {'slug': 'slug'}, 1),
])
def test_404_ok(my_model, my_user, post_id, kwargs, objects):
    post = get_object_or_404(objects, **kwargs)
    assert post.id == post_id
