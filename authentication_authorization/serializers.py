from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import Group, Permission


class GroupsSerializer(ModelSerializer):
    class Meta:
        model = Group
        # fields = '__all__'
        fields = ('id', 'name', 'permissions',)
        read_only_fields = ('id',)


class PermissionSerializer(ModelSerializer):
    class Meta:
        model = Permission
        fields = ('id', 'name', 'codename', 'content_type',)
        read_only_fields = ('id',)
