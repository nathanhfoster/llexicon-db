from rest_framework.permissions import AllowAny
from django.db.models import Q
from rest_framework import serializers
from rest_framework.filters import SearchFilter

from .models import Specialization, Skill, SpecializationSkillExperience
from rest_framework import viewsets, permissions
from .serializers import SpecializationSerializer, SkillSerializer, SpecializationSkillExperienceSerializer


class SpecializationView(viewsets.ModelViewSet):
    serializer_class = SpecializationSerializer
    queryset = Specialization.objects.all()
    permission_classes = (AllowAny,)


class SkillView(viewsets.ModelViewSet):
    serializer_class = SkillSerializer
    queryset = Skill.objects.all()
    permission_classes = (AllowAny,)


class SpecializationSkillExperienceView(viewsets.ModelViewSet):
    serializer_class = SpecializationSkillExperienceSerializer
    queryset = SpecializationSkillExperience.objects.all()
    permission_classes = (AllowAny,)
    filter_backends = (SearchFilter, )
    search_fields = ('author__id', 'id')
