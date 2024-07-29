from rest_framework import permissions


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return request.user.is_superuser


class IsSelfOrSuperUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        if request.user.is_staff or request.user.is_superuser:
            return True
        
        if request.user.id == obj.id:
            return True
        
        return False


class UnauthenticatedOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_authenticated
