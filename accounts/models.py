# We'll use Django's built-in User model
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # Add additional user fields if needed
    
    def __str__(self):
        return self.user.username
