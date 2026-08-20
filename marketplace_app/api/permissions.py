from rest_framework.permissions import BasePermission


class IsAuthenticatedBusinessUser(BasePermission):
    """Allow access only to authenticated business users."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.type == "business"
        )

class IsOfferOwner(BasePermission):
    """Allow changes only when the offer belongs to the user."""

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and obj.user == request.user
        )
