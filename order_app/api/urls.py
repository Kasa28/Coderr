from django.urls import path
from order_app.api.views import OrdersView

urlpatterns = [
    path("orders/", OrdersView.as_view(), name="order-list-create"),
]