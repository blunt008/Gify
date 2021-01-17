from django.contrib import admin
from .models import User, Avatar, Profile


class AvatarInline(admin.StackedInline):
    model = Avatar
    max_num = 1

class ProfileInline(admin.ModelAdmin):
    inlines = [AvatarInline]

class UserAdmin(admin.ModelAdmin):
    inlines = [
        ProfileInline
    ]


admin.site.register(User)
admin.site.register(Profile, ProfileInline)
admin.site.register(Avatar)
