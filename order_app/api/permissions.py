from rest_framework.permissions import BasePermission

class CheckIsCustomerUser(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.type == "customer"
        )


class CheckIsBusinessUser(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.type == "business"
        )


class CheckBusinessOwnsOrder(BasePermission):

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

    def has_object_permission(
        self,
        request,
        view,
        order,
    ):
        user_is_customer = order.customer_user == request.user
        user_is_business = order.business_user == request.user

        return user_is_customer or user_is_business
