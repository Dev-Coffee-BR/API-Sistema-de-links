from rest_framework.permissions import BasePermission


class IsNotDeletedUser(BasePermission):
    """
    Allows access to verified users only.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.soft_delet == None
        )


class ReadOnly(BasePermission):
    """
    Allows access to read only.
    """

    def has_permission(self, request, view):
        return bool(request.method in ["GET", "HEAD", "OPTIONS"])
