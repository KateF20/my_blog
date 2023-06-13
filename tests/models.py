from django.db import models
from django.conf import settings


class MyModel(models.Model):
    slug = models.SlugField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        app_label = 'tests'
