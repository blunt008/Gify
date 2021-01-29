from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post

# Create your views here.

def index(request):
    """
    Index page
    """
    posts = Post.objects.all()
    paginator = Paginator(posts, 3)
    page = request.GET.get("page", "")
    try:
        posts = paginator.page(page)
        if request.META["CONTENT_TYPE"] == "application/json":
            return render(
                request,
                "gify/list_ajax.html",
                {"posts": posts}
            )
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
        return HttpResponse("")

    return render(request,
                  "gify/home.html",
                  {"section": "index", "posts": posts})

