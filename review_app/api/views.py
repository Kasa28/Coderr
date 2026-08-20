from rest_framework import filters, generics
from rest_framework.permissions import (AllowAny, IsAuthenticated)
from django_filters.rest_framework import (DjangoFilterBackend)
from review_app.api.filters import FilterForReview
from review_app.api.permissions import CheckIsCustomerUser, CheckIsUserOwnsReview
from review_app.api.serializers import SerializerForReview, WhenReviewUpdateSerializerAllowThisFields
from review_app.models import Review

class ReviewsView(generics.ListCreateAPIView):
    """List reviews or create a review as a customer."""

    serializer_class = SerializerForReview

    queryset = Review.objects.select_related("reviewer", "business_user").all()

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]

    filterset_class = FilterForReview

    ordering_fields = ["updated_at", "rating"]
    ordering = ["-updated_at"]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), CheckIsCustomerUser()]

        return [AllowAny()]


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve a review or let its author update and delete it."""

    queryset = Review.objects.all()
    serializer_class = WhenReviewUpdateSerializerAllowThisFields

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]

        return [
            IsAuthenticated(),
            CheckIsUserOwnsReview(),
        ]
