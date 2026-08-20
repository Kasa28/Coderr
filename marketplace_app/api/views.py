from django.contrib.auth import get_user_model
from django.db.models import Avg, Min
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from marketplace_app.api.filters import OfferFilter
from marketplace_app.api.paginations import OffersResultPagination
from marketplace_app.api.permissions import IsAuthenticatedBusinessUser, IsOfferOwner
from marketplace_app.api.serializers import OfferSerializer, OfferPackageSerializer
from marketplace_app.models import MarketplaceOffer, OfferPackage
from review_app.models import Review

User = get_user_model()

class OffersListView(generics.ListCreateAPIView):
    """List all offers or create an offer as a business user."""

    serializer_class = OfferSerializer
    pagination_class = OffersResultPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = OfferFilter
    search_fields = ["title", "description"]
    ordering_fields = ["updated_at", "min_price"]
    ordering = ["-updated_at"]

    def get_queryset(self):
        return (
            MarketplaceOffer.objects
            .select_related("user")
            .prefetch_related("packages")
            .annotate(
                min_price=Min("packages__price"),
                min_delivery_time=Min(
                    "packages__delivery_time_in_days"
                ),
            )
        )

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), IsAuthenticatedBusinessUser()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve an offer or let its owner update and delete it."""

    serializer_class = OfferSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]

        return [
            IsAuthenticated(),
            IsOfferOwner(),
        ]

    def get_queryset(self):
        return (
            MarketplaceOffer.objects
            .select_related("user")
            .prefetch_related("packages")
            .annotate(
                min_price=Min("packages__price"),
                min_delivery_time=Min(
                    "packages__delivery_time_in_days"
                ),
            )
        )

class OfferPackageDetailView(generics.RetrieveAPIView):
    """Retrieve one offer package by its ID."""

    queryset = OfferPackage.objects.select_related(
        "offer",
        "offer__user",
    )
    serializer_class = OfferPackageSerializer
    permission_classes = [IsAuthenticated]


class MarketplaceStatisticsView(APIView):
    """Return marketplace counts and the average review rating."""

    
    permission_classes = [AllowAny]

    def get(self, request):
        offer_count = MarketplaceOffer.objects.count()
        review_count = Review.objects.count()
        business_count = User.objects.filter(type="business").count()
        rating_data = Review.objects.aggregate(average=Avg("rating"))
        average_rating = rating_data["average"]

        if average_rating is None:
            average_rating = 0
        else:
            average_rating = round(average_rating, 1)

        return Response({
            "offer_count": offer_count,
            "review_count": review_count,
            "business_profile_count": business_count,
            "average_rating": average_rating,
        })
