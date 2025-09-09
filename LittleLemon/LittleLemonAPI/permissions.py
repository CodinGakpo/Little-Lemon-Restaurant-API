from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser or request.user.groups.filter(name="Manager").exists()

class IsManagerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_superuser or request.user.groups.filter(name="Manager").exists()

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_superuser or request.user.groups.filter(name='Manager').exists()
