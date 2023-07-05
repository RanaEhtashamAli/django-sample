from rest_framework.permissions import BasePermission
from user.models import User


class PatientPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.user_role == User.UserRoleEnums.PATIENT:
            return True
        return False
