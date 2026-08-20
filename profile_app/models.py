from django.conf import settings
from django.db import models

class Profile(models.Model):
    """Store public profile information belonging to one user."""

    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    file = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True,
    )

    location = models.CharField(
        max_length=300,
        blank=True,
        default="",
    )

    tel = models.CharField(
        max_length=30,
        blank=True,
        default="",
    )

    description = models.TextField(
        blank=True,
        default="",
    )

    working_hours = models.CharField(
        max_length=140,
        blank=True,
        default="",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "profile"
        verbose_name_plural = "profiles"
        ordering = ["user__username"]

    def __str__(self):
        return f"Profile of {self.user.username}"
