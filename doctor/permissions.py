from rest_framework.permissions import BasePermission
from user.models import User


class DoctorPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.user_role == User.UserRoleEnums.DOCTOR:
            return True
        return False
