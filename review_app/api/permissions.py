from rest_framework.permissions import BasePermission

class CheckIsCustomerUser(BasePermission):
    """Allow access only to authenticated customer users."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.type == "customer"
        )


class CheckIsUserOwnsReview(BasePermission):
    """Allow changes only when the review belongs to the user."""

    def has_object_permission(
        self,
        request,
        view,
        review,
    ):
        return review.reviewer == request.user
