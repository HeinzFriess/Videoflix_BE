from django.db import models
from datetime import date


# Create your models here.
class Video(models.Model):
    created_at = models.DateField(default=date.today)
    title = models.CharField(max_length=80)
    category = models.CharField(max_length=80, blank=True, null=True)
    description = models.CharField(max_length=500)
    video_file = models.FileField(upload_to="videos/", blank=True, null=True)
    video_file360p = models.FileField(upload_to="videos/", blank=True, null=True)
    video_file720p = models.FileField(upload_to="videos/", blank=True, null=True)
    video_file1080p = models.FileField(upload_to="videos/", blank=True, null=True)
    video_fileThumbnail = models.FileField(
        upload_to="thumbnails/", blank=True, null=True
    )

    def __str__(self) -> str:
        return self.title
