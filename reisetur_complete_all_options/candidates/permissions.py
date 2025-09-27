from rest_framework import permissions

class IsAdminOrCreateOnly(permissions.BasePermission):
    """Allow anyone to create (POST) a candidate, but only staff can view/list/modify."""
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return bool(request.user and request.user.is_staff)

class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)
