from rest_framework import permissions

class IsAdminOrOwnerPermission(permissions.BasePermission):
    """Разрешение только для администратора или автора"""

    def has_object_permission(self, request, view, obj):

        if request.user.is_stuff or request.user.is_superuser or obj.id == request.user.pk:
            return bool(True)

class IsOwnerPermission(permissions.BasePermission):
    """Разрешение только для автора."""

    def has_object_permission(self, request, view, obj):
        return bool(obj.id == request.user.pk)
