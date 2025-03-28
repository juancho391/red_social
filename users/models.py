# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    description  = models.TextField(null=True, blank=True)
    profile_img = models.CharField(null=True, blank=True)
    birth_date = models.DateTimeField(null=False)