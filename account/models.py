from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from network.settings import STATIC_URL

from django.conf import settings


class User(AbstractUser):
    pass


class Profile(models.Model):

    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name="profile")
    username = models.CharField(max_length=20)
    title = models.CharField(max_length=40)
    about = models.CharField(max_length=255)
    joined = models.DateField(auto_now_add=True)
    facebook_url = models.URLField(max_length=40, default='')
    twitter_url = models.URLField(max_length=40, default='')
    github_url = models.URLField(max_length=40, default='')
    youtube_url = models.URLField(max_length=40, default='')

    def __repr__(self):
        return f"Profile: {self.username}"

    def __str__(self):
        return f"Profile: {self.username}"

    def change_avatar(self, avatar) -> None:
        """ 
        Change avatar by unselecting current one and setting
        'selected = True' to the avatar in the formal parameter
        """
        self.unselect_avatar()
        avatar.selected = True
        avatar.save()

    def get_avatar(self):
        avatar = self.avatars.get(selected=True).avatar

        return avatar

    def unselect_avatar(self):
        try:
            avatar = self.avatars.get(selected=True)
            avatar.selected = False
            avatar.save()
        except Avatar.DoesNotExist:
            pass
    
    def set_default_avatar(self) -> None:
        """
        Change user avatar to default if last custom avatar was deleted
        """
        try:
            avatar = self.avatars.first()
            avatar.selected = True
            avatar.save()
        except Avatar.DoesNotExist:
            pass

    def validate_urls(self, urls: dict) -> bool:
        """
        Check if URLs received are valid URLs.
        """
        url_validator = URLValidator()
        for value in urls.values():
            try:
                url_validator(value)
            except ValidationError:
                return False
        
        return True     

    def update_social_urls(self, urls: dict) -> None:
        """
        Update user's profile with the social URLs received
        """
        facebook_url = urls.get('facebook', '')
        twitter_url = urls.get('twitter', '')
        github_url = urls.get('github', '')
        youtube_url = urls.get('youtube', '')

        self.facebook_url = facebook_url
        self.twitter_url = twitter_url
        self.github_url = github_url
        self.youtube_url = youtube_url

        self.save()

        
class Avatar(models.Model):

    user = models.ForeignKey(
        Profile,
        related_name="avatars",
        on_delete=models.CASCADE
    )

    avatar = models.ImageField(upload_to="users/%Y/%m/%d/",
                               default="no-avatar.png")
    selected = models.BooleanField(default=True)
    added = models.DateTimeField(auto_now_add=True)

    def __repr__(self):
        return f"Avatar for user {self.user.username}"

    def __str__(self):
        return f"Avatar for user {self.user.username}"

    class Meta:
        
        ordering = ["added"]
