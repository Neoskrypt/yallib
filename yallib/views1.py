from django.views.generic import TemplateView
from yallib.models import Author


class AuthorView(TemplateView):
    template_name = 'authors.html'
    model = Author

    def get_context_data(self, *args, **kwargs):
        context = super(AuthorView, self).get_context_data(**kwargs)
        context["Authors"] = Author.objects.filter(pk=self.kwargs.get("id"))
        # return render(self.request, self.template_name, context)
        return context


class AuthorListView(AuthorView):
    def get_context_data(self, *args, **kwargs):
        context = super(AuthorView, self).get_context_data(**kwargs)
        context["Authors"] = Author.objects.all()
        return context
