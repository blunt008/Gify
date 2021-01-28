from django.shortcuts import render

from .models import Video

# Create your views here.

def index(request):
    """
    Index page
    """
    videos = Video.objects.all()
    return render(request,
                  "gify/home.html",
                  {"section": "index", "videos": videos})

