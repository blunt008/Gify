from django import forms
from .models import Post


class PostCreateForm(forms.ModelForm):
    """
    Form for creating new entries
    """
    class Meta:
        model = Post
        fields = ("link",)

    def clean_link(self):
        """
        Check if the link provided points
        to streamable or youtube and raise validation errors
        if it doesn't
        """
        link = self.cleaned_data.get("link", "");
        print(link)
        if "you" not in link and "stream" not in link:
            print("error")
            raise forms.ValidationError(("We only accept URLs to YouTube"
                                         " or Streamable"))

        return link

