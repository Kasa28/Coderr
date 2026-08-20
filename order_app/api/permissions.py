from rest_framework.permissions import BasePermission

class CheckIsCustomerUser(BasePermission):
    """Allow access only to authenticated customer users."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.type == "customer"
        )


class CheckIsBusinessUser(BasePermission):
    """Allow access only to authenticated business users."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.type == "business"
        )


class CheckBusinessOwnsOrder(BasePermission):
    """Allow changes only to the business user receiving the order."""

    def has_object_permission(
        self,
        request,
        view,
        order,
    ):
        return (
            order.business_user == request.user
        )


class UserCanViewOrder(BasePermission):
    """Allow an order to be viewed by its customer or business user."""

    def has_object_permission(
        self,
        request,
        view,
        order,
    ):
        user_is_customer = order.customer_user == request.user
        user_is_business = order.business_user == request.user

        return user_is_customer or user_is_business
