from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from account.models import Profile

from account.models import Profile


class Post(models.Model):
    profile = models.ForeignKey(
        Profile,
        related_name="posts",
        on_delete=models.CASCADE
    )
    user_likes = models.ManyToManyField(
        Profile,
        related_name='posts_likes',
        blank=True)
    link = models.URLField()
    created = models.DateField(
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"Post created: {self.created}"


class Comment(models.Model):
    author = models.CharField(max_length=255)
    post = models.ForeignKey(
        Post,
        related_name='comments',
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)
    body = models.CharField(max_length=250)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.body}'


class Action(models.Model):

    profile = models.ForeignKey(Profile,
                             related_name='actions',
                             db_index=True,
                             on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)
    target_ct = models.ForeignKey(ContentType,
                                  blank=True,
                                  null=True,
                                  related_name='target_obj',
                                  on_delete=models.CASCADE)
    target_id = models.PositiveIntegerField(null=True,
                                            blank=True,
                                            db_index=True)
    target = GenericForeignKey('target_ct', 'target_id')
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)
    url = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.profile.username} {self.verb}'
