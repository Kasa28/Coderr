from django.db import models
from django.contrib.auth.models import AbstractUser



class CoderrUser(AbstractUser):
    """Custom user account with a customer or business role."""

    USER_TYPES = [
        ("customer", "Customer"),
        ("business", "Business"),
    ]

    type = models.CharField(max_length=50, choices=USER_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ["username"]

    def __str__(self):
        return self.username
