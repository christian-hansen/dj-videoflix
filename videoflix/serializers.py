from rest_framework import serializers
from videoflix.models import Video
import os

class VideoItemSerializer(serializers.ModelSerializer):
    video_file_360p = serializers.SerializerMethodField()
    video_file_720p = serializers.SerializerMethodField()
    video_file_1080p = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = "__all__"

    def get_video_file_360p(self, obj):
        return self.get_converted_video_path(obj, '360p')

    def get_video_file_720p(self, obj):
        return self.get_converted_video_path(obj, '720p')

    def get_video_file_1080p(self, obj):
        return self.get_converted_video_path(obj, '1080p')

    def get_converted_video_path(self, obj, resolution):
        """
        Construct the path for the converted video file.
        """
        if obj.video_file:
            base, ext = os.path.splitext(obj.video_file.url)
            return f"{base}_{resolution}{ext}"
        return None