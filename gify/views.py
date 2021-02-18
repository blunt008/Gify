from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required 

from .models import Post
from .forms import PostCreateForm

# Create your views here.


@login_required
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


@login_required
def post_create(request):
    """
    View for handling post creation
    """
    if request.method == "POST":
        # form is sent
        form = PostCreateForm(data=request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            link = cleaned_data.get("link", "")
            print(link)
        else:
            return JsonResponse({
                "status": "error",
                "errors": form.errors.as_json()
            }, safe=False, status=422)
    else:
        form = PostCreateForm()

    return render(
        request,
        "gify/create.html",
        {"form": form}
    )
