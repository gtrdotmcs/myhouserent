from rest_framework import permissions

class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'OWNER'

class IsTenant(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'TENANT'

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and (request.user.is_superuser or request.user.role == 'OWNER')

class IsTenantOrOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and (request.user.is_superuser or request.user.role == 'OWNER' or request.user.role == 'TENANT')
