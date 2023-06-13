from django.http import Http404
from django.db.models import QuerySet


def get_object_or_404(model, **kwargs):
    if isinstance(model, QuerySet):
        query_set = model
        model = query_set.model
    else:
        query_set = model.objects

    try:
        obj = query_set.get(**kwargs)

    except model.DoesNotExist:
        raise Http404(f'No {model} matches the given {kwargs.keys()}.')

    return obj
