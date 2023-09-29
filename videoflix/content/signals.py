import os
import django_rq
from content.tasks import convert480p, convert720p
from .models import Video
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    # Get the path to the Video file
    Video_file_path = instance.video_file.path

    if created:
        queue = django_rq.get_queue('default',autocommit=True)
        queue.enqueue(convert480p, Video_file_path)
        queue.enqueue(convert720p, Video_file_path)
        #convert480p(Video_file_path)
        #convert720p(Video_file_path)
        #print('New Video created')


@receiver(pre_delete, sender=Video)
def video_pre_delete(sender, instance, using, **kwargs):
    # Get the path to the Video file
    Video_file_path = instance.video_file.path

    # Check if the file exists and delete it
    if os.path.isfile(Video_file_path):
        os.remove(Video_file_path)
        print('deleted')
