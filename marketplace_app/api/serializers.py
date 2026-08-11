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
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

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

    def get_min_price(self, obj):
        prices = [package.price for package in obj.packages.all()]
        return min(prices) if prices else None

    def get_min_delivery_time(self, obj):
        delivery_times = [
            package.delivery_time_in_days
            for package in obj.packages.all()
        ]
        return min(delivery_times) if delivery_times else None

    def create(self, validated_data):
        packages_data = validated_data.pop("packages")
        offer = MarketplaceOffer.objects.create(**validated_data)

        for package_data in packages_data:
            OfferPackage.objects.create(
                offer=offer,
                **package_data,
            )

        return offer
