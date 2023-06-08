from django.db import models


class MyModel(models.Model):
    slug = models.SlugField(max_length=50)

    class Meta:
        app_label = 'tests'
