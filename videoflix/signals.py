from .models import Video
from .tasks import convert_360p
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import os


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    print('Video was saved')
    if created:
        print('Video was created')
        video_path = instance.video_file.path
        convert_360p(video_path)


@receiver(post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes the video file from the filesystem
    when corresponding 'Video' object uis deleted.
    """
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)
            # os.remove(instance.video_file.path) #TODO 360p
            # os.remove(instance.video_file.path) #TODO 720p
            # os.remove(instance.video_file.path) #TODO 1080p
