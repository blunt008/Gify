from django.shortcuts import render

from .models import Post

# Create your views here.

def index(request):
    """
    Index page
    """
    videos = Post.objects.all()
    return render(request,
                  "gify/home.html",
                  {"section": "index", "videos": videos})

