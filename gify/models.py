from django.db import models
from django.conf import settings
from account.models import Profile

# Create your models here.

class Post(models.Model):
    profile = models.ForeignKey(
        Profile,
        related_name="posts",
        on_delete=models.CASCADE
    )
    link = models.URLField()
    created = models.DateField(
        auto_now_add=True,
        db_index=True
    )

    def __str__(self):
        return f"Post created: {self.created}"


class Comment(models.Model):
    author = models.ForeignKey(
        Profile,
        related_name='comments',
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post,
        related_name='comments',
        on_delete=models.CASCADE
    )
    text = models.CharField(max_length=250)
