from django_filters import rest_framework as filters
from marketplace_app.models import MarketplaceOffer


class OfferFilter(filters.FilterSet):
    creator_id = filters.NumberFilter(field_name="user_id")
    max_delivery_time = filters.NumberFilter(
        field_name="packages__delivery_time_in_days",
        lookup_expr="lte",
        distinct=True,
    )

    class Meta:
        model = MarketplaceOffer
        fields = ["creator_id", "max_delivery_time"]
