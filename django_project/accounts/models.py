from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(models.Model):
    username = models.TextField()
    password = models.TextField()