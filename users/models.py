# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    description = models.TextField(null=True, blank=True)
    profile_img = models.CharField(max_length=100, null=True, blank=True)
    birth_date = models.DateTimeField(null=False)
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_set",  # Cambia a un nombre único
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_permission_user_set",  # Cambia a un nombre único
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )
