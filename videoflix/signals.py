from .models import Video
from .tasks import convert_video
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import os

from django_rq import enqueue
import django_rq




@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    print('Video was saved')
    if created:
        # print('Video was created')
        video_path = instance.video_file.path
        # print(video_path)
        queue = django_rq.get_queue('default', autocommit=True)
        # print('Start queue')
        # Enqueue tasks for 360p, 720p, and 1080p
        queue.enqueue(convert_video, video_path, '360p')
        queue.enqueue(convert_video, video_path, '720p')
        queue.enqueue(convert_video, video_path, '1080p')
        # print('Finished queue')
       


@receiver(post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes the video file and its converted versions from the filesystem
    when the corresponding 'Video' object is deleted.
    """
    if instance.video_file:
        video_path = instance.video_file.path

        # List of resolutions
        resolutions = ['360p', '720p', '1080p']

        # Delete the original file
        if os.path.isfile(video_path):
            os.remove(video_path)

        # TODO Delete Thumbnail
        
        # Delete the converted files
        for resolution in resolutions:
            converted_file_path = f"{os.path.splitext(video_path)[0]}_{resolution}.mp4"
            print('Deleting, ', converted_file_path)
            if os.path.isfile(converted_file_path):
                os.remove(converted_file_path)
