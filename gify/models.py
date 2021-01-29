from django.db import models
from embed_video.fields import EmbedVideoField

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=20)
    link = models.URLField()
