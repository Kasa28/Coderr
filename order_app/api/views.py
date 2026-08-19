from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from order_app.api.permissions import CheckIsCustomerUser
from order_app.api.serializers import OrderListCreateSerializer
from order_app.models import Order


class OrdersView(generics.ListCreateAPIView):
    serializer_class = OrderListCreateSerializer

    def get_queryset(self):
        user = self.request.user

        if user.type == "customer":
            return Order.objects.filter(
                customer_user=user
            ).order_by("-created_at")

        if user.type == "business":
            return Order.objects.filter(
                business_user=user
            ).order_by("-created_at")

        return Order.objects.none()

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), CheckIsCustomerUser()]
        return [IsAuthenticated()]