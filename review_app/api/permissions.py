from rest_framework.permissions import BasePermission

class CheckIsCustomerUser(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.type == "customer"
        )


class CheckIsUserOwnsReview(BasePermission):

    def has_object_permission(
        self,
        request,
        view,
        review,
    ):
        return review.reviewer == request.user