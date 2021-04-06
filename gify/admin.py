from django.contrib import admin
from .models import Post, Action

# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["created"]
    list_filter = ["created"]


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('profile', 'verb', 'target', 'created')
    list_filter = ('created',)
    search_fields = ('verb',)
