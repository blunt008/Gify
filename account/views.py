import json

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.contrib.auth import authenticate, login 
from django.contrib.auth.views import (LoginView, PasswordChangeView,
                                        PasswordResetView,
                                        PasswordResetDoneView,
                                        PasswordResetConfirmView)
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils.translation import gettext, gettext_lazy as _
from django.utils.decorators import method_decorator
from common.decorators import redirect_if_logged_in
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.files import File
from django.db.models import ProtectedError
from django import forms 
from network.settings import STATIC_URL

from easy_thumbnails.files import get_thumbnailer

from .forms import (LoginForm, ChangePasswordForm,
                    UserRegistrationForm,
                    EditUserForm, MyPasswordResetForm, 
                    MyPasswordResetConfirmForm)
from .models import Avatar, Profile
from gify.utils import create_action


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    """
    Custom view for confirming new passwords
    """
    form_class = MyPasswordResetConfirmForm


class MyPasswordResetView(PasswordResetView):
    """
    Custom password reset view to use custom html template 
    and custom password reset form
    """
    template_name = "registration/password_reset_form.html"
    form_class = MyPasswordResetForm


@method_decorator(redirect_if_logged_in, name='dispatch')
class MyLoginView(LoginView):
    """
    Custom Login View, uses LoginForm as its authentication form. 
    Decorated with 'redirect_if_logged_in' to redirect logged in users 
    from common routes such as 'register'
    """
    authentication_form = LoginForm

class MyPasswordChangeView(PasswordChangeView):
    """
    Custom Password Change View, uses ChangePasswordForm as its form class. 
    """
    form_class = ChangePasswordForm


def register(request: HttpRequest) -> HttpResponse:
    """
    View function for handling user registration
    """
    if request.method == "POST":
        user_form = UserRegistrationForm(data=request.POST, files=request.FILES)
        if user_form.is_valid():
            avatar = request.FILES.get("avatar")
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data["password"]
            )
            new_user.save()
            new_user_profile = Profile.objects.create(user=new_user,
                                                      username=new_user.username)
            if avatar:
                Avatar.objects.create(user=new_user_profile, avatar=avatar)
            else:
                Avatar.objects.create(user=new_user_profile)

            return render(request,
                          "account/register_done.html",
                          { "new_user": new_user})
    else:
        user_form = UserRegistrationForm()

    return render(
        request,
        "account/register.html",
        {"user_form": user_form}
    )

@login_required
def profile(request: HttpRequest, name: str) -> HttpResponse:
    """
    View function for displaying user profiles
    """
    user_profile = get_object_or_404(Profile, user__username=name)

    return render(
        request,
        "account/profile-new.html",
        {'section': 'profile', "user_profile": user_profile}
    )

@login_required
def edit_profile(request: HttpRequest, name: str) -> HttpResponse:
    """ 
    Display edit page for current user and save any changes to the profile.
    Only for logged in users
    """
    user_profile = get_object_or_404(Profile, user__username=name)
    avatar_count = user_profile.avatars.count()

    if user_profile != request.user.profile:
        return redirect("gify:index")

    if request.method == "POST":
        form = EditUserForm(request.POST, instance=user_profile)
        avatar = request.FILES.get("avatar", None)
        if form.is_valid():
            edited_profile = form.save()
            if avatar:
                edited_profile.unselect_avatar()
                Avatar.objects.create(user=edited_profile, avatar=avatar)
            return redirect(reverse("account:profile", args=[user_profile.username]))
    else:
        form = EditUserForm(instance=user_profile)

    return render(
        request,
        "account/edit_profile-new.html",
        {
            "section": "edit",
            "user_profile": user_profile,
            "form": form,
            "avatar_count": avatar_count
        }
    )


@login_required
@require_POST
def get_avatars(request: HttpRequest) -> HttpResponse:
    """
    Handle AJAX requests requesting all avatars for the
    single user.
    """
    SKIP_FIRST_AVATAR = 1
    payload = json.loads(request.body)
    profile_id = payload.get("id")
    profile = Profile.objects.get(pk=profile_id)
    avatars = profile.avatars.all()[SKIP_FIRST_AVATAR:]

    response = JsonResponse({
        "status": "ok",
        "avatars": [
            {
                "id": avatar.id,
                "url": avatar.avatar.url
            }
            for avatar in avatars
        ]
    }, safe=False)
    response.status_code = 200
    return response

@login_required
@require_POST
def change_avatar(request: HttpRequest) -> HttpResponse:
    """
    Handle AJAX requests requesting avatar change
    """
    payload = json.loads(request.body)
    avatar_id = payload.get("id", "")

    try:
        avatar = Avatar.objects.get(id=avatar_id)
        request.user.profile.change_avatar(avatar)
    except Avatar.DoesNotExist:
        avatar = None

    if avatar:
        response = JsonResponse({
            "status": "ok",
            "url": avatar.avatar.url
        })
        response.status_code = 200
        return response
    else:
        response = JsonResponse({
            "status": "Error when handling avatar change"
        })
        response.status_code = 500
        return response

@login_required
@require_POST
def delete_avatar(request):
    """
    Handle AJAX requests requesting avatar deletion
    """
    payload = json.loads(request.body)
    avatar_id = payload.get("id", "")

    try:
        avatar = Avatar.objects.get(id=avatar_id)
        user_profile = request.user.profile
        is_current = avatar.selected
    except (Avatar.DoesNotExist, Profile.DoesNotExists):
        avatar = None
        user_profile = None
        is_current = False

    if is_current:
        user_profile.set_default_avatar()
        thumbnailer = get_thumbnailer(avatar.avatar)
        thumbnailer.delete_thumbnails()
        avatar.delete()
        response = JsonResponse({
            "status": "ok",
            "selected": True
        })
        response.status_code = 201
        return response

    if avatar and user_profile:
        try:
            thumbnailer = get_thumbnailer(avatar.avatar)
            thumbnailer.delete_thumbnails()
            avatar.delete()
            return JsonResponse({
                "status": "ok",
            })
        except ProtectedError:
            return JsonResponse({
                "status": "error"
            })
    else:
        response = JsonResponse({
            "status": "Error when handling avatar deletion"
        })
        response.status_code = 500
        return response



@login_required
@require_POST
def update_social(request):
    """
    Handle AJAX requests updating user's social URLs
    """
    profile = request.user.profile
    body = json.loads(request.body)
    if profile.validate_urls(body):
        profile.update_social_urls(body)
        return JsonResponse({'status': 'ok'}, status=201)
    else:
        return JsonResponse({'status': "Error updating social profiles. Check your links..."}, status=422)


@login_required
@require_POST
def follow_unfollow(request):
    """
    Handle follow / unfollow logic. Requests
    sent via AJAX
    """
    body_parsed = json.loads(request.body)
    profile_id_to_follow = body_parsed.get('profile_id', None)
    action = body_parsed.get('action', None)

    profile_to_follow = Profile.objects.get(id=profile_id_to_follow)

    if action and profile_to_follow:
        if action == 'follow':
            request.user.profile.following.add(profile_id_to_follow)
            create_action(request.user.profile,
                          'is following',
                          profile_to_follow)
        elif action == 'unfollow':
            request.user.profile.following.remove(profile_id_to_follow)
        return JsonResponse({'status': 'ok'}, status=200)
    return JsonResponse({'status': f'Error handling "{action}" action'},
                         status=422)
