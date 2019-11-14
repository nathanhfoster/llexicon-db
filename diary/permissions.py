from rest_framework import permissions
from .models import Entry


class IsAuthorOrSuperUser(permissions.BasePermission):
    """
    Custom permission to only allow users to edit their own profile
    """

    def has_permission(self, request, view):
        user = request.user
        userId = None

        if user.is_superuser:
            return True

        elif('pk' in view.request.query_params):
            userId = view.request.query_params['pk']
            
        elif('pk' in view.kwargs):
            userId = view.kwargs['pk']

       

        try:
            entry_profile = Entry.objects.get(author=userId)
            if user == entry_profile.author:
                return True
        except:
            # If the user was not found then return false
            return False


class IsStaffOrTargetUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # allow user to list all users if logged in user is staff
        return view.action == 'retrieve' or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # allow logged in user to view own details, allows staff to view all records
        return request.user.is_staff or obj == request.user
