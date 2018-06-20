from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.contrib import auth
#  csrf_protect-декоратор обеспечивающий защиту CsrfViewMiddleware
from yallib.models import Author
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login/')
def get_authors(request):
    return render(request, 'authors.html', {"Authors": Author.objects.all(),
                                            "username": request.user.email})


@login_required(login_url='/login/')
def get_author(request, id):
    return render(request, 'authors.html', {"Authors": Author.objects.filter(pk=id),
                                            "username": request.user.email})


@csrf_protect
def login(request):
    args = {}
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("/")
        else:
            args["login_error"] = "User not found!!!"
            return render(request, "login.html", args)
    else:
        return render(request, "login.html", args)


class TestView(TemplateView):
    template_name = 'login.html'
    http_method_names = ['post']

    def post(self, *args, **kwargs):

        return render(self.request, self.template_name)


























# def logout(request):
    # logout(request)
    # return redirect("/")
