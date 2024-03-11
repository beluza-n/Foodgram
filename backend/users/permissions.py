from rest_framework.permissions import BasePermission


class MeIsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        if view.action == 'me':
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        if view.action == 'me':
            return request.user.is_authenticated
        return True
