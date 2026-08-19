from django.urls import path
from order_app.api.views import OrdersView, OrderDetailView

urlpatterns = [
    path("orders/", OrdersView.as_view(), name="order-list-create"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
]