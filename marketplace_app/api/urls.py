from django.urls import path
from marketplace_app.api.views import OffersListView, OfferDetailView, OfferPackageDetailView

urlpatterns = [
    path('offers/', OffersListView.as_view(), name='offer-list'),
    path('offers/<int:pk>/', OfferDetailView.as_view(), name='offer-detail'),
    path('offerdetails/<int:pk>/', OfferPackageDetailView.as_view(), name='offer-package-detail'),
]
