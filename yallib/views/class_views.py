from django.views.generic import TemplateView
from yallib.models import Author, Book
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.utils.decorators import method_decorator


def indexHtml(request):
    """
    this func for home page of the site
    """
    # generate counts some of the main objects
    num_book = Book.objects.all().count()
    num_authors = Author.objects.count()
    num_visitors = request.session.get("num_visitors", 0)
    request.session["num_visitors"] = num_visitors+1

    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={"num_book": num_book, "num_visitors": num_visitors},
    )


# @login_required(login_url='/login/')
# @method_decorator(login_required, name="login_url")
class AuthorView(TemplateView):
    template_name = 'authors.html'
    model = Author

    @method_decorator(login_required(login_url='/login/'))
    def get_context_data(request, *args, **kwargs):
        context = super(AuthorView, request).get_context_data(**kwargs)
        context["Authors"] = Author.objects.filter(pk=request.kwargs.get("id"))
        # return render(self.request, self.template_name, context)
        return context


# @method_decorator(login_required)
class AuthorListView(AuthorView):
    paginate_by = 10

    @method_decorator(login_required(login_url='/login/'))
    def get_context_data(request, *args, **kwargs):
        context = super(AuthorView, request).get_context_data(**kwargs)
        context["Authors"] = Author.objects.all()
        return context


class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    initial = {"date_birth": "09/07/2018", }


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = ["first_name", "last_name", "date_birth"]


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy("authorlist")
