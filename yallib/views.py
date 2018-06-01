from django.http import HttpResponse
from django.shortcuts import render_to_response,redirect
from django.contrib.auth import authenticate,login,logout
from django.template.context_processors import csrf

from yallib.models import Author

def get_authors(request):
    return render_to_response('authors.html',{"Authors":Author.objects.all(),"username":auth.get_user(request).username})
def login(request):
    args = {}
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get("username","")
        password = request.POST.get("password","")
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect("/")
        else:
            args["login_error"] = "User not found!!!"
            return render_to_response("login.html",args)
    else:
        return render_to_response("login.html",args)
#def logout(request):
    #logout(request)
    #return redirect("/")
