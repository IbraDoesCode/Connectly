from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, default='')
    last_name = models.CharField(max_length=30, default='')
    bio = models.TextField(blank=True, default='')

    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username