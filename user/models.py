from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField('username', max_length=50, unique=True)
    password = models.CharField('password', max_length=50)

    def __str__(self):
        return self.username
