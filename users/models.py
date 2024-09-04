from django.db import models
from django.contrib.auth.models import AbstractUser
from videoflix.models import Video

# Create your models here.
class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=500)
    # favorites = models.ManyToManyField(Video, blank=True, related_name='favorited_by')
    
    def __str__(self) -> str:
        return f'({self.id}) - {self.username} - {self.first_name} {self.last_name}'