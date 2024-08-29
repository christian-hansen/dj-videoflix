from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=500)
    phone = models.CharField(max_length=15, blank=True, null=True)
    custom = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)   
    
    def __str__(self) -> str:
        return f'({self.id}) - {self.username} - {self.first_name} {self.last_name}'