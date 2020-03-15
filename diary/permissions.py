from rest_framework import permissions
from .models import Entry
from django.db.models import Q


class IsAuthorOrSuperUser(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user

        # print("view: ", view.action)

        if user.is_superuser:
            return True

        entryId = view.kwargs['pk']

        # print('entryId: ', entryId)

        entry = Entry.objects.get(pk=entryId)

        if entry.is_public and view.action == 'details':
            return True
        elif entry.author == user:
            return True

        return False


class IsStaffOrTargetUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # allow user to list all users if logged in user is staff
        return view.action == 'retrieve' or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # allow logged in user to view own details, allows staff to view all records
        return request.user.is_staff or obj == request.user
