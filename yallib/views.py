from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response

from yallib.models import Author

def get_authors(request):
    return render_to_response('authors.html',{"Author":Author.objects.all()})

def get_authors1(request):
    data = {
            'first_name': request.GET.get('first_name'),
            'last_name': request.GET.get('last_name'),
            'date_birth': request.GET.get('date_birth')
    }

    t = get_template('authors.html')
    html = t.render(Context(data))
    return HttpResponse(html)

def get_authors2(request):
    return render_to_response('authors.html',{'first_name': request.GET.get('first_name'),
    'last_name': request.GET.get('last_name'),
    'date_birth': request.GET.get('date_birth')})
def get_authors3(request):
    return render(request,'authors.html',context={"Author":Author.objects.all()})
