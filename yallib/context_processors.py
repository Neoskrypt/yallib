from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.context_processors import request


def menu(request):

    return {
        "site_name": settings.SITE_NAME,
        "site_description": settings.SITE_DESCRIPTION
        }


def view_authors(request):
    return render_to_response('authors.html',
        RequestContext(request, processors=[menu]))


def view_login(request):
    return render_to_response('login.html',
        RequestContext(request, processors=[menu]))


def view_register(request):
    return render_to_response('register.html',
        RequestContext(request, processors=[menu]))
