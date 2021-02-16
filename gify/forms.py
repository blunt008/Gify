from django import forms
from .models import Post


class PostCreateForm(forms.modelForm):
    """
    Form for creating new entries
    """
    class Meta:
        model = Post
        fields = ("created", "url")
