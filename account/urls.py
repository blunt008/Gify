from django.urls import path
from django.contrib.auth import views as auth_views

from . import views 
from . import forms

urlpatterns = [
            path("register/", views.register, name="register"),
            path('login/', views.MyLoginView.as_view(),name='login'),
            path('logout/', auth_views.LogoutView.as_view(), name='logout'),
            path('password_change/',
                 views.MyPasswordChangeView.as_view(),
                 name='password_change'),
            path('password_change/done/',
                 auth_views.PasswordChangeDoneView.as_view(), 
                 name='password_change_done'),
            path("password_reset/",
                 views.MyPasswordResetView.as_view(),
                 name="password_reset"),
            path("password_reset/done/",
                 auth_views.PasswordResetDoneView.as_view(),
                 name="password_reset_done"),
            path("reset/<uidb64>/<token>/",
                 views.MyPasswordResetConfirmView.as_view(),
                 name="password_reset_confirm"),
            path("reset/done/",
                 auth_views.PasswordResetCompleteView.as_view(
                     template_name="registration/password_reset_complete.html"
                 ),
                 name="password_reset_complete"),
            path("change_avatar/", views.change_avatar, name="change_avatar"),
            path("profile/<str:name>/",
                 views.profile,
                 name="profile"),
            path("edit/profile/<str:name>/",
                 views.edit_profile, name="edit_profile"),
            path("avatars/", views.get_avatars, name="get_avatars"),
            path("delete_avatar/", views.delete_avatar, name="delete_avatar"),
        ]
