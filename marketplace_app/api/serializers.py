from rest_framework import serializers

from marketplace_app.models import OfferPackage


class OfferPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferPackage
        fields = [
            "id",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
        ]