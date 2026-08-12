from django.urls import path
from marketplace_app.api.views import OffersListView

urlpatterns = [
    path('offers/', OffersListView.as_view(), name='offer-list')
]
