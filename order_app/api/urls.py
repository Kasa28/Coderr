from django.urls import path
from order_app.api.views import OrdersView, OrderDetailView,CompletedOrdersCountView, OpenOrdersCountView

urlpatterns = [
    path("orders/", OrdersView.as_view(), name="order-list-create"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
    path("order-count/<int:user_id>/", OpenOrdersCountView.as_view(), name="open-orders-count"),
    path("completed-order-count/<int:user_id>/", CompletedOrdersCountView.as_view(), name="completed-orders-count"),

]