from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    profile_image = models.ImageField(upload_to = 'profiles/', blank = True, null = True)
    introduce = models.TextField(blank = True)
    followings = models.ManyToManyField('self', symmetrical = False, related_name = 'followers', blank = True)
    