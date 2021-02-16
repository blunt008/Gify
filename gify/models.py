from django.db import models
from django.conf import settings

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
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
