from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.contrib import auth
#  csrf_protect-декоратор обеспечивающий защиту CsrfViewMiddleware
from yallib.models import Author


def get_authors(request):
    return render_to_response('\
    authors.html', {"Authors": Author.objects.all(), "\
    username": auth.get_user(request).get_username()})


def get_author(request, id):
    return render_to_response('\
    authors.html', {"Authors": Author.objects.filter(pk=id), "\
    username": auth.get_user(request).get_username()})


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
            return render_to_response("login.html", args)
    else:
        return render_to_response("login.html", args)
# def logout(request):
    # logout(request)
    # return redirect("/")
