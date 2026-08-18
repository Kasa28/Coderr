from django.db.models import Min
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from marketplace_app.api.filters import OfferFilter
from marketplace_app.api.paginations import OffersResultPagination
from marketplace_app.api.permissions import IsAuthenticatedBusinessUser
from marketplace_app.api.serializers import OfferSerializer
from marketplace_app.models import MarketplaceOffer


class OffersListView(generics.ListCreateAPIView):
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


class OfferDetailView(generics.RetrieveAPIView):
    serializer_class = OfferSerializer
    permission_classes = [AllowAny]

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