from rest_framework.permissions import BasePermission

class IsDoctorUser(BasePermission):
    """
    Allows access only to users with the role 'doctor'.
    """
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.roles == 'doctor'
