import json

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .models import Post, Comment, Action
from .forms import PostCreateForm, CommentForm
from .utils import create_action


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
def wall(request):
    """
    Handle logic for wall view
    """
    actions = Action.objects.exclude(profile=request.user.profile)
    following_ids = request.user.profile.following.values_list('id', flat=True)

    if following_ids:
        actions = actions.filter(profile_id__in=following_ids)

    actions = actions[:10]
    return render(request,
                  "gify/wall.html",
                  {"section": "wall", "actions": actions})


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
            create_action(user_profile, 'created post', new_post, new_post.link)
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


@require_POST
def add_comment(request):
    post_id = request.POST.get('post_id', None)
    post = get_object_or_404(Post, id=post_id)
    comment_form = CommentForm(data=request.POST)
    if comment_form.is_valid():
        new_comment = comment_form.save(commit=False)
        new_comment.post = post
        new_comment.author = request.user.username
        new_comment.save()
        create_action(request.user.profile, 'commented on', new_comment,
                      new_comment.post.link)
        return JsonResponse({'comment': {
            'author': request.user.username,
            'body': new_comment.body,
            'created': new_comment.created
        }}, status=201)
    else:
        errors = comment_form.errors.get_json_data(escape_html=True)
        return JsonResponse(errors, status=422)


@login_required
@require_POST
def like_unlike(request):
    """
    Handle liking / unliking posts AJAX logic
    """
    body_parsed = json.loads(request.body)
    post_id = body_parsed.get('id', None)
    action = body_parsed.get('action', None)
    post = Post.objects.get(id=post_id)

    if post:
        if action == 'like':
            post.user_likes.add(request.user.profile)
        else:
            post.user_likes.remove(request.user.profile)
        return JsonResponse({'status': 'ok'}, status=200)
    return JsonResponse({'status': 'error'}, status=422)
