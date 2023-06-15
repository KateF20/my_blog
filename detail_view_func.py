from django.http import HttpResponseNotAllowed, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.views import View


class DetailView(View):
    template_name = None
    model = None
    url = None
    MyForm = None
    context_object_name = None
    slug_field = 'slug'
    kwargs_pk_name = 'id'
    kwargs_slug_name = 'slug'

    def setup(self):
        pass

    def dispatch(self):
        pass

    def get_object(self):
        pk = self.kwargs.get(self.kwargs_pk_name)
        slug = self.kwargs.get(self.kwargs_slug_name)

        try:
            if pk is not None:
                return self.model.objects.get(pk=pk)
            elif slug is not None:
                return self.model.objects.get(**{self.slug_field: slug})
            else:
                raise ImproperlyConfigured("")
        except self.model.DoesNotExist:
            raise Http404('No such object')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def render_to_response(self, context):
        return 

    def get_context_data(self, **kwargs):
        kwargs[self.get_context_object_name()] = kwargs['object']
        return kwargs

    def http_method_not_allowed(self):
        return HttpResponseNotAllowed('Allowed methods are: GET, POST ???')

    def get_template_names(self):
        return self.template_name

    def get_queryset(self):
        pass

    def get_context_object_name(self):
        if self.context_object_name:
            return self.context_object_name
        else:
            return self.model.__name__.lower()

    def get_absolute_url(self):
        return reverse(self.url, kwargs={'slug': self.object.slug})
