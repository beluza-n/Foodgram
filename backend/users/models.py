from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    REQUIRED_FIELDS = ["email", "first_name", 'last_name']
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

