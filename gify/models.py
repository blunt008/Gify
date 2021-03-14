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
    post = models.ForeignKey(
        Post,
        related_name='comments',
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)
    body = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.text}'
