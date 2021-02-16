from django.urls import path

from . import views 

app_name = "gify"

urlpatterns = [
    path("create/", views.post_create, name="create"),
    path("", views.index, name="index"),
]
