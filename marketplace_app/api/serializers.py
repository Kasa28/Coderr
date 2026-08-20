from rest_framework import serializers
from marketplace_app.models import MarketplaceOffer, OfferPackage

class OfferPackageSerializer(serializers.ModelSerializer):
    """Serialize the data of an individual offer package."""

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


class OfferSerializer(serializers.ModelSerializer):
    """Serialize offers together with their nested packages."""

    details = OfferPackageSerializer(
        source="packages",
        many=True,
    )
    min_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )
    min_delivery_time = serializers.IntegerField(read_only=True)

    class Meta:
        model = MarketplaceOffer
        fields = [
            "id",
            "user",
            "title",
            "description",
            "image",
            "details",
            "min_price",
            "min_delivery_time",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "min_price",
            "min_delivery_time",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        """Create an offer and all packages submitted with it."""
        packages_data = validated_data.pop("packages")
        offer = MarketplaceOffer.objects.create(**validated_data)

        for package_data in packages_data:
            OfferPackage.objects.create(
                offer=offer,
                **package_data,
            )
        return offer

    
    def update(self, offer, validated_data):
        """Update an offer and the submitted package data."""
        package_list = validated_data.pop("packages", [])
        updated_offer = super().update(
            offer,
            validated_data,
        )

        for package_data in package_list:
            offer_type = package_data["offer_type"]
            package = updated_offer.packages.get(
                offer_type=offer_type,
            )

            if "title" in package_data:
                package.title = package_data["title"]

            if "revisions" in package_data:
                package.revisions = package_data["revisions"]

            if "delivery_time_in_days" in package_data:
                package.delivery_time_in_days = (
                    package_data["delivery_time_in_days"]
                )

            if "price" in package_data:
                package.price = package_data["price"]

            if "features" in package_data:
                package.features = package_data["features"]

            package.save()
        return updated_offer
