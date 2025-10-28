from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    currency = models.CharField(max_length=10, default="PKR")
    
    def __str__(self):
        return self.user.username

