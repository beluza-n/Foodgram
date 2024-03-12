from rest_framework.permissions import BasePermission


class MeIsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated if view.action == 'me' else True

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated if view.action == 'me' else True
