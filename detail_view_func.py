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

    def setup(self):
        pass

    def dispatch(self):
        pass

    def get_object(self):
        slug = self.kwargs.get('slug')
        try:
            return self.model.objects.get(slug=slug)

        except self.model.DoesNotExist:
            raise Http404('No such object')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.MyForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.object.get_absolute_url())
        context = self.get_context_data()
        return self.render_to_response(context)

    def http_method_not_allowed(self):
        return HttpResponseNotAllowed('Allowed methods are: GET, POST ???')

    def get_template_names(self):
        return self.template_name

    def get_slug_field(self):
        pass

    def get_queryset(self):
        pass

    def get_context_object_name(self):
        if self.context_object_name:
            return self.context_object_name
        else:
            return self.model.__name__.lower()

    def get_context_data(self):
        context = {}
        context[str(self.get_context_object_name())] = self.get_object()
        return context

    def get_absolute_url(self):
        return reverse(self.url, kwargs={'slug': self.object.slug})
