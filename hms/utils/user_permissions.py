from rest_framework import permissions


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return False


class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return False


class IsPatient(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_patient:
            return True
        return False
