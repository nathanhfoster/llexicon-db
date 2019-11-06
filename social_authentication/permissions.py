from rest_framework import permissions
from user.models import User


class IsAuthorOrSuperUser(permissions.BasePermission):
    """
    Custom permission to only allow users to edit their own profile
    """

    def has_permission(self, request, view):
        userId = view.kwargs['pk']
        if request.user.is_staff or request.user.is_superuser:
            return True
        # print(view.kwargs)
        # print(request.user.id)
        # Look for the requested user in the database
        try:
            user_profile = User.objects.get(
                pk=userId)
        except:
            # If the user was not found then return false
            return False

        # Check that the requesting user id matches the authenticated user id
        # print(request.user)
        # print(user_profile)
        if request.user == user_profile:
            return True
        return False


class IsStaffOrTargetUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # allow user to list all users if logged in user is staff
        return view.action == 'retrieve' or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # allow logged in user to view own details, allows staff to view all records
        return request.user.is_staff or obj == request.user
