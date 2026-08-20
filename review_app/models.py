from django.conf import settings
from django.core.validators import (MaxValueValidator, MinValueValidator)
from django.db import models

class Review(models.Model):
    """Store a customer's rating and review of a business user."""


    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews_made",
    )

    business_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews_received",
    )

    rating = models.IntegerField(
        validators=[
            MinValueValidator(1), MaxValueValidator(5),
        ],
    )

    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "review"
        verbose_name_plural = "reviews"
        ordering = ["-updated_at"]
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "reviewer", "business_user",
                ],
                name="one_review_per_business_user",
            )
        ]


    def __str__(self):
        return f"{self.reviewer} -> {self.business_user}: {self.rating}/5"
