from django.shortcuts import render
from .models import Blogpost


from django.http import HttpResponse
# Create your views here.
def index(request):
    mypost=Blogpost.objects.all()
    params={"mypost":mypost}
    return render(request,'blog/index.html',params)
def blogpost(request,id):
    post=Blogpost.objects.filter(id=id)[0]
    dic={'post':post}

    return render(request,'blog/blogpos.html',dic)