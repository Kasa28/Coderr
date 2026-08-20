from django_filters import rest_framework as filters
from review_app.models import Review

class FilterForReview(filters.FilterSet):
    """Filter reviews by reviewed business user or review author."""

    business_user_id = filters.NumberFilter(field_name="business_user_id")

    reviewer_id = filters.NumberFilter(field_name="reviewer_id")

    class Meta:
        model = Review
        fields = ["business_user_id", "reviewer_id"]
