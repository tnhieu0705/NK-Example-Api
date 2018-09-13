from example_2.base.constants.common import AppConstants
from rest_framework.permissions import BasePermission, IsAuthenticated


class IsAdmin(BasePermission):
    message = 'Require ADMIN role.'

    def has_permission(self, request, view):
        return request.user.id and request.user.role_id == AppConstants.Role.Admin


class IsUser(BasePermission):
    message = 'Require USER role.'

    def has_permission(self, request, view):
        return request.user.id and request.user.role_id == AppConstants.Role.User


class IsCustomer(BasePermission):
    message = 'Require CUSTOMER role.'

    def has_permission(self, request, view):
        return request.user.id and request.user.role_id == AppConstants.Role.Customer


class AllowOptionsAuthentication(IsAuthenticated):

    def has_permission(self, request, view):
        if request.method == 'OPTIONS':
            return True
        return request.user and request.user.is_authenticated
