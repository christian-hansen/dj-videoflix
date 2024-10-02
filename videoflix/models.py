from django.db import models
from datetime import date

# Genre model
class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
# Video model
class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    created_at = models.DateField(default=date.today)
    video_file = models.FileField(upload_to='videos', blank=True, null=True)
    thumbnail_file = models.FileField(upload_to='thumbnails', blank=True, null=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'({self.id}) - {self.title}'
