from django.contrib.auth.models import AbstractUser
from django.db import models
from network.settings import STATIC_URL

from django.conf import settings


class User(AbstractUser):
    pass


class Profile(models.Model):

    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name="profile")
    username = models.CharField(max_length=20)
    about = models.CharField(max_length=50)
    joined = models.DateField(auto_now_add=True)

    def __repr__(self):
        return f"Profile: {self.username}"

    def __str__(self):
        return f"Profile: {self.username}"

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
