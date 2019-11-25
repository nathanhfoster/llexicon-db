from rest_framework import permissions
from .models import Entry
from django.db.models import Q


class IsAuthorOrSuperUser(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user

        # print("User: ", user)

        if user.is_superuser:
            return True

        entryId = view.kwargs['pk']

        # print('entryId: ', entryId)

        entry_profile = Entry.objects.all().filter(Q(pk=entryId), Q(author=user))

        # print("entry_profile: ", entry_profile)

        if entry_profile.count() > 0:
            return True

        return False


class IsStaffOrTargetUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # allow user to list all users if logged in user is staff
        return view.action == 'retrieve' or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # allow logged in user to view own details, allows staff to view all records
        return request.user.is_staff or obj == request.user
