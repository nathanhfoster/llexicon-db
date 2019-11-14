from rest_framework import permissions
from user.models import User


class IsAuthorOrSuperUser(permissions.BasePermission):
    """
    Custom permission to only allow users to edit their own profile
    """

    def has_permission(self, request, view):
        user = request.user

        if user.is_superuser:
            return True

        elif('pk' in view.kwargs):
            userId = view.kwargs['pk']
            try:
                user_profile = User.objects.get(pk=userId)
                if user == user_profile:
                    return True
            except:
                # If the user was not found then return false
                return False

        else:
            return False


class IsStaffOrTargetUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # allow user to list all users if logged in user is staff
        return view.action == 'retrieve' or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # allow logged in user to view own details, allows staff to view all records
        return request.user.is_staff or obj == request.user
