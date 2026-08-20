from django_filters import rest_framework as filters
from marketplace_app.models import MarketplaceOffer

class OfferFilter(filters.FilterSet):
    """Filter offers by creator and maximum package delivery time."""

    creator_id = filters.NumberFilter(field_name="user_id")
    min_price = filters.NumberFilter(field_name="min_price", lookup_expr="gte")
    max_delivery_time = filters.NumberFilter(
        field_name="packages__delivery_time_in_days",
        lookup_expr="lte",
        distinct=True,
    )

    class Meta:
        model = MarketplaceOffer
        fields = ["creator_id", "min_price", "max_delivery_time"]
