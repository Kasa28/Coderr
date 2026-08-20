from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsProfileOwnerOrReadOnly(BasePermission):
    """Allow profile changes only when the profile belongs to the user."""

    def has_object_permission(self, request, view, obj): 
        return request.user == obj.user
