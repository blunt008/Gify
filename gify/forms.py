from django import forms
from .models import Post


class PostCreateForm(forms.ModelForm):
    """
    Form for creating new entries
    """
    class Meta:
        model = Post
        fields = ("link",)

    def clean_url(self):
        """
        Check if the link provided links
        to streamable or youtube. In such case
        transform it into 'embedded' version and
        if not show error
        """
        url = self.cleaned_data["url"]
        print(url)
