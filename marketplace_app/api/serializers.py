from rest_framework import serializers
from marketplace_app.models import MarketplaceOffer, OfferPackage

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


class OfferSerializer(serializers.ModelSerializer):
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
        packages_data = validated_data.pop("packages")
        offer = MarketplaceOffer.objects.create(**validated_data)

        for package_data in packages_data:
            OfferPackage.objects.create(
                offer=offer,
                **package_data,
            )

        return offer
