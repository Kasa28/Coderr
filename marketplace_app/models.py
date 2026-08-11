from django.db import models
from django.conf import settings


class MarketplaceOffer(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="marketplace_offers",
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(
        upload_to="marketplace_offers/",
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class OfferPackage(models.Model):
    OFFER_TYPE_CHOICES = [
        ("basic", "Basic"),
        ("standard", "Standard"),
        ("premium", "Premium"),
    ]

    offer = models.ForeignKey(
        MarketplaceOffer,
        on_delete=models.CASCADE,
        related_name="packages",
    )

    title = models.CharField(max_length=200)
    revisions = models.IntegerField()
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=list)
    offer_type = models.CharField(
        max_length=20,
        choices=OFFER_TYPE_CHOICES,
    )

    def __str__(self):
        return f"{self.offer.title} – {self.get_offer_type_display()}"
# Create your models here.
