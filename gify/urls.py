from django.urls import path

from . import views 

app_name = "gify"

urlpatterns = [
    path("create/", views.post_create, name="create"),
    path("get_comments/", views.retrieve_comments, name="get_comments"),
    path("", views.index, name="index"),
]
