from django.http import HttpResponse
from django.shortcuts import render_to_response

from yallib.models import Author

def get_authors(request):
    return render_to_response('authors.html',{"Authors":Author.objects.all()})
