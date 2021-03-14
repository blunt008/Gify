from django import forms
from .models import Post, Comment


class PostCreateForm(forms.ModelForm):
    """
    Form for creating new entries
    """
    class Meta:
        model = Post
        fields = ("link",)

    def clean_link(self):
        """
        Check if URL links to supported service and transform it
        to embedded version
        """
        link = self.cleaned_data.get("link", "");

        if "you" in link:
            link = self.youtube_embed(link)
        elif "stream" in link:
            link = self.streamable_embed(link)
        else:
            raise forms.ValidationError(("We only accept URLs to YouTube"
                                         " or Streamable"))

        return link

    def youtube_embed(self, url: str) -> str:
        """
        Transform standard youtube URL
        into embedded version
        """
        YOUTUBE_EMBED_URL = "https://www.youtube.com/embed/"
        link_id = url.split("/")[-1]
        if "?" in link_id:
            link_id = link_id.split("?")[0]

        return YOUTUBE_EMBED_URL + link_id

    def streamable_embed(self, url: str) -> str:
        """
        Transform standard streamable URL
        into embedded version
        """
        STREAMABLE_EMBED_URL = "https://streamable.com/e/"
        link_id = url.split("/")[-1]

        return STREAMABLE_EMBED_URL + link_id


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
