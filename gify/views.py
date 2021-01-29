from django.shortcuts import render

from .models import Video

# Create your views here.

def index(request):
    """
    Index page
    """
    videos = Video.objects.all()[:3]
    return render(request,
                  "gify/home.html",
                  {"section": "index", "videos": videos})

