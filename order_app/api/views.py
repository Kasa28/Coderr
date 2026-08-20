from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from order_app.api.permissions import CheckIsCustomerUser, CheckBusinessOwnsOrder, CheckIsBusinessUser, UserCanViewOrder
from order_app.api.serializers import OrderListCreateSerializer, OrderStatusSerializer
from order_app.models import Order
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

User = get_user_model()

class OrdersView(generics.ListCreateAPIView):
    """List the user's orders or create an order as a customer."""

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


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete an order with the required permission."""

    queryset = Order.objects.all()
    serializer_class = OrderStatusSerializer



    def get_permissions(self):
        if self.request.method == "DELETE":
            return [IsAuthenticated(), IsAdminUser()]

        if self.request.method in ["PUT", "PATCH"]:
            return [
                IsAuthenticated(),
                CheckIsBusinessUser(),
                CheckBusinessOwnsOrder(),
            ]
        return [IsAuthenticated(), UserCanViewOrder()]
    

class OpenOrdersCountView(APIView):
    """Return the number of open orders for one business user."""

    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        business_user = get_object_or_404(
            User,
            id=user_id,
            type="business",
        )

        open_orders = Order.objects.filter(
            business_user=business_user,
            status="in_progress",
        )

        number_of_open_orders = open_orders.count()

        return Response({
            "order_count": number_of_open_orders,
        })


class CompletedOrdersCountView(APIView):
    """Return the number of completed orders for one business user."""
    
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        business_user = get_object_or_404(
            User,
            id=user_id,
            type="business",
        )

        completed_orders = Order.objects.filter(
            business_user=business_user,
            status="completed",
        )

        number_of_completed_orders = (
            completed_orders.count()
        )

        return Response({
            "completed_order_count": number_of_completed_orders,
        })
