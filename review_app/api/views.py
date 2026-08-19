from rest_framework import filters, generics
from rest_framework.permissions import (AllowAny, IsAuthenticated)
from django_filters.rest_framework import (DjangoFilterBackend)
from review_app.api.filters import FilterForReview
from review_app.api.permissions import CheckIsCustomerUser
from review_app.api.serializers import SerializerForReview
from review_app.models import Review

class ReviewsView(generics.ListCreateAPIView):
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
