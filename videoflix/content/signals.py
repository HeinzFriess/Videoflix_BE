import os
import django_rq
from content.tasks import convert360p, convert720p, convert1080p, createThumbnail
from .models import Video
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    if created:
        queue = django_rq.get_queue('default',autocommit=True)
        # Get the path to the Video file
        video_file_path = instance.video_file.path
        video_file_name = instance.video_file.name

        instance.video_fileThumbnail.name = video_file_path.replace(".mp4", ".jpg")
        queue.enqueue(createThumbnail, video_file_path, instance.video_fileThumbnail.path)
        instance.video_fileThumbnail.name = video_file_name.replace(".mp4", ".jpg")
        
        instance.video_file360p.name = video_file_path.replace(".mp4", "_360p.mp4")
        queue.enqueue(convert360p, video_file_path, instance.video_file360p.path)
        instance.video_file360p.name = video_file_name.replace(".mp4", "_360p.mp4")

        instance.video_file720p.name = video_file_path.replace(".mp4", "_720p.mp4")
        queue.enqueue(convert720p, video_file_path, instance.video_file720p.path)
        instance.video_file720p.name = video_file_name.replace(".mp4", "_720p.mp4")

        instance.video_file1080p.name = video_file_path.replace(".mp4", "_1080p.mp4")
        queue.enqueue(convert1080p, video_file_path, instance.video_file1080p.path)
        instance.video_file1080p.name = video_file_name.replace(".mp4", "_1080p.mp4")

        instance.save()


@receiver(pre_delete, sender=Video)
def video_pre_delete(sender, instance, using, **kwargs):
    
    # Check if the file exists and delete it
    if os.path.isfile(instance.video_file1080p.path):
        os.remove(instance.video_file1080p.path)

    if os.path.isfile(instance.video_file720p.path):
        os.remove(instance.video_file720p.path)

    if os.path.isfile(instance.video_file360p.path):
        os.remove(instance.video_file360p.path)
        
    if os.path.isfile(instance.video_file.path):
        os.remove(instance.video_file.path)

    if os.path.isfile(instance.video_fileThumbnail.path):
        os.remove(instance.video_fileThumbnail.path)