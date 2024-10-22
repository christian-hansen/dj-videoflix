from rest_framework import serializers
from videoflix.models import Video, Genre
import os


# Serializer for Genre
class GenreItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class VideoItemSerializer(serializers.ModelSerializer):
    video_file_360p = serializers.SerializerMethodField()
    video_file_720p = serializers.SerializerMethodField()
    # video_file_1080p = serializers.SerializerMethodField()
    genre = serializers.SerializerMethodField()
    class Meta:
        model = Video
        fields = ['id', 'video_file_360p', 'video_file_720p', 'title', 'description', 'created_at', 'video_file', 'thumbnail_file', 'genre']
        
    def get_genre(self, obj):
        # Return the genre name, if genre is not None
        return obj.genre.name if obj.genre else None

    def get_video_file_360p(self, obj):
        return self.get_converted_video_path(obj, '360p')

    def get_video_file_720p(self, obj):
        return self.get_converted_video_path(obj, '720p')

    # def get_video_file_1080p(self, obj):
    #     return self.get_converted_video_path(obj, '1080p')

    def get_converted_video_path(self, obj, resolution):
        """
        Construct the path for the converted video file.
        """
        if obj.video_file:
            base, ext = os.path.splitext(obj.video_file.url)
            return f"{base}_{resolution}{ext}"
        return None