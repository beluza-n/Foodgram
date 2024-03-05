from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth import get_user_model


class CustomUser(AbstractUser):
    REQUIRED_FIELDS = ["email", "first_name", 'last_name']
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    class Meta:
        app_label = 'users'
        verbose_name = ("user")
        verbose_name_plural = ("users")

    def __str__(self):
        return self.email

User = get_user_model()

class UserFollowing(models.Model):
    user = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    following_user = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user','following_user'],  name="unique_followers")
        ]
        ordering = ["-created"]

    def __str__(self):
        f"{self.user} follows {self.following_user}"
