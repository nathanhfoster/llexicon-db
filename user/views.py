from rest_framework.permissions import AllowAny
from django.db.models import F
from rest_framework import serializers

from django.contrib.auth.models import Group
from .models import User, Setting
from rest_framework import viewsets, permissions
from .serializers import UserSerializer, SettingSerializer, SettingViewSerializer, Serializer, AdminSerializer
from user.permissions import IsUpdateProfile, IsStaffOrTargetUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django.utils.timezone import now
from django.contrib.auth.models import update_last_login
from django.contrib.auth import get_user_model
import json


class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (SearchFilter, )
    search_fields = ('id', 'profile_uri')

    def get_permissions(self):

        # allow an authenticated user to create via POST
        if self.request.method == 'GET':
            self.permission_classes = (AllowAny,)
        if self.request.method == 'POST':
            self.permission_classes = (AllowAny,)
        if self.request.method == 'PATCH':
            self.permission_classes = (
                permissions.IsAuthenticated, IsUpdateProfile,)
        return super(UserView, self).get_permissions()

    @action(methods=['get'], detail=True, permission_classes=[permission_classes])
    def profile(self, request, pk):
        qs = User.objects.get(profile_uri=pk)

        return Response(UserSerializer(qs).data)

    @action(methods=['get'], detail=True, permission_classes=[permission_classes])
    def refresh(self, request, pk):
        qs = User.objects.get(pk=pk)

        if request.user and request.user.is_authenticated:
            user = request.user
            user.last_login = now()
            user.save(update_fields=['last_login'])

        return Response(Serializer(qs).data)

    @action(methods=['get'], detail=False, permission_classes=[permission_classes])
    def all(self, request):
        qs = User.objects.all()
        serializer = AdminSerializer(qs, many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def addEducation(self, request, pk):
        education = json.loads(request.data['education'])
        user = get_user_model().objects.get(id=pk)
        user.education.clear()
        user.education.set(education)
        return Response(json.dumps(education))

    @action(methods=['post'], detail=True)
    def addSkills(self, request, pk):
        technical_skills = json.loads(request.data['technical_skills'])
        user = get_user_model().objects.get(id=pk)
        user.technical_skills.clear()
        user.technical_skills.set(technical_skills)
        return Response(json.dumps(technical_skills))

    @action(methods=['post'], detail=True)
    def addExperience(self, request, pk):
        experience = json.loads(request.data['experience'])
        user = get_user_model().objects.get(id=pk)
        user.experience.clear()
        user.experience.set(experience)
        return Response(json.dumps(experience))


class SettingView(viewsets.ModelViewSet):
    serializer_class = SettingSerializer
    queryset = Setting.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_permissions(self):
        # allow an authenticated user to create via POST
        if self.request.method == 'GET':
            self.permission_classes = (permissions.IsAuthenticated,)
        if self.request.method == 'PATCH':
            self.permission_classes = (
                permissions.IsAuthenticated,)
        return super(SettingView, self).get_permissions()

    @action(methods=['get'], detail=True, permission_classes=[permission_classes])
    def view(self, request, pk):
        queryset = Setting.objects.all().filter(user=pk)

        serializer = SettingViewSerializer(queryset, many=True)

        if serializer.data:
            return Response(serializer.data[0])
        else:
            return Response({'show_footer': True, 'push_messages': False})
