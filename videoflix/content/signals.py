import os
import django_rq
from content.tasks import convert360p, convert720p, convert1080p, createThumbnail
from .models import Video
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    # Get the path to the Video file
    Video_file_path = instance.video_file.path

    if created:
        queue = django_rq.get_queue('default',autocommit=True)
        queue.enqueue(convert360p, Video_file_path)
        instance.video_file360p = Video_file_path.replace(".mp4", "_360p.mp4")
        queue.enqueue(convert720p, Video_file_path)
        instance.video_file720p = Video_file_path.replace(".mp4", "_720p.mp4")
        queue.enqueue(convert1080p, Video_file_path)
        instance.video_file1080p = Video_file_path.replace(".mp4", "_1080p.mp4")
        queue.enqueue(createThumbnail, Video_file_path)
        instance.video_fileThumbnail = Video_file_path.replace(".mp4", ".jpg")
    
    instance.save()


@receiver(pre_delete, sender=Video)
def video_pre_delete(sender, instance, using, **kwargs):
    
    # Check if the file exists and delete it
    if os.path.isfile(instance.video_file.path):
        os.remove(instance.video_file.path)

    if os.path.isfile(instance.video_file1080p):
        os.remove(instance.video_file1080p)

    if os.path.isfile(instance.video_file720p):
        os.remove(instance.video_file720p)

    if os.path.isfile(instance.video_file360p):
        os.remove(instance.video_file360p)

    if os.path.isfile(instance.video_fileThumbnail):
        os.remove(instance.video_fileThumbnail)