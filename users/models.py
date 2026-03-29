from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Email is the login field; extend with profile fields in Phase 2 as needed."""

    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self) -> str:
        return self.email
