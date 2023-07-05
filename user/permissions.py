from rest_framework.permissions import BasePermission


class CustomPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.id == int(view.kwargs['pk']):
            return True
        return False
