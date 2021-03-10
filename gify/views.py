from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required 

from .models import Post, Comment
from .forms import PostCreateForm


# Create your views here.


@login_required
def index(request):
    """
    GIFy homepage
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
            user_profile = request.user.profile
            new_post = form.save(commit=False)
            new_post.profile = user_profile
            new_post.save()
            return JsonResponse({
                "status": "ok",
                "link": new_post.link,
                'id': new_post.id
            }, status=201)
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


def retrieve_comments(request):
    """
    View function to handle Ajax requests for 
    retrieving comments under post
    """
    post_id = request.GET.get('post', 0)
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()

    return render(request,
                  'gify/list_comment_ajax.html',
                  {'comments': comments})
