from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminAllOrAuthenticatedReadOnly(BasePermission):
    """
    The request is authenticated as an admin - read/write,
    if as a user - read-only request
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_staff
