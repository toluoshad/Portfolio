from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):  # Extending Django's built-in user model
    email = models.EmailField(unique=True)  # Make email unique

    def __str__(self):
        return self.username
