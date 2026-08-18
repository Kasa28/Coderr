from django.urls import path
from marketplace_app.api.views import OffersListView, OfferDetailView

urlpatterns = [
    path('offers/', OffersListView.as_view(), name='offer-list'),
    path('offers/<int:pk>/', OfferDetailView.as_view(), name='offer-detail'),
]
