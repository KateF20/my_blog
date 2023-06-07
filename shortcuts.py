from django.http import Http404


def get_object_or_404(model, **kwargs):
    try:
        obj = model.objects.get(**kwargs)

    except model.DoesNotExist:
        raise Http404(f'No {model} matches the given {kwargs.keys()}.')

    return obj
