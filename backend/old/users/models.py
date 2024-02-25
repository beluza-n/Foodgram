from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
#     REQUIRED_FIELDS = ["email", "first_name", "last_name"]
    pass

    # def __str__(self):
    #     return self.username
