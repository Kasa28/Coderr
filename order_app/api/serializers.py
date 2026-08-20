from rest_framework import serializers
from marketplace_app.models import OfferPackage
from order_app.models import Order


class OrderListCreateSerializer(serializers.ModelSerializer):
    """List orders and create an order from a selected package."""

    offer_detail_id = serializers.PrimaryKeyRelatedField(
        queryset=OfferPackage.objects.all(),
        source="offer_detail",
        write_only=True,
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
            "updated_at",
            "offer_detail_id",
        ]

        read_only_fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        """Create an order by copying the selected package data."""
        selected_package = validated_data.pop(
            "offer_detail"
        )
        customer_user = self.context["request"].user
        business_user = selected_package.offer.user

        return Order.objects.create(
            customer_user=customer_user,
            business_user=business_user,
            offer_detail=selected_package,
            title=selected_package.title,
            revisions=selected_package.revisions,
            delivery_time_in_days=(
                selected_package.delivery_time_in_days
            ),
            price=selected_package.price,
            features=selected_package.features,
            offer_type=selected_package.offer_type,
            status="in_progress",
        )


class OrderStatusSerializer(serializers.ModelSerializer):
    """Return order details while allowing only its status to change."""

    status = serializers.ChoiceField(
        choices=Order.STATUS_CHOICES,
        required=True,
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "created_at",
            "updated_at",
        ]
