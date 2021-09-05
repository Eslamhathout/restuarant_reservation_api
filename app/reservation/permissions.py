from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Check if user an admin"""

    message = 'This action can only be made by admin users.'
    def has_permission(self, request, view):
        return request.user.role == 'Admin'
