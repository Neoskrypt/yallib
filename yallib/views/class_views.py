from django.views.generic import TemplateView
from yallib.models import Author, Book
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView
from django.views.generic.base import RedirectView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import REDIRECT_FIELD_NAME, login, logout as auth_logout
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
import urllib.parse
from django.conf import settings


class LoginView(FormView):

    form_class = AuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'login.html'

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        """
        The user has provided valid credentials (this
        was checked in AuthenticationForm.is_valid()). So now we
        can log him in.
        """
        login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        if self.success_url:
            redirect_to = self.seccess_url
        else:
            redirect_to = self.request.REQUEST.get(self.redirect_field_name, "")

        netloc = urllib.parse.urllib.parse(redirect_to)[1]
        if not redirect_to:
            redirect_to = settings.LOGIN_REDIRECT_URL
        # Security check -- don't allow redirection to a different host.
        elif netloc and netloc != self.request.get_host():
            redirect_to = settings.LOGIN_REDIRECT_URL
            return redirect_to

    def set_test_cookie(self):
        self.request.session.set_test_cookie()

    def check_and_delete_test_cookie(self):
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
            return True
        return False

    def get(self, request, *args, **kwargs):
        """
        Same as django.views.generic.edit.ProcessFormView.get(),
        but adds test cookie stuff
        """
        self.set_test_cookie()
        return super(LoginView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Same as django.views.generic.edit.ProcessFormView.post(),
        but adds test cookie stuff
        """
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            self.check_and_delete_test_cookie()
            return self.form_valid(form)
        else:
            self.set_test_cookie()
            return self.form_invalid(form)


class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = ''

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


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
