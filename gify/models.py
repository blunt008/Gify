from django.db import models
from embed_video.fields import EmbedVideoField

# Create your models here.

class Video(models.Model):
    title = models.CharField(max_length=20)
    video = EmbedVideoField()
