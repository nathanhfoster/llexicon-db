from rest_framework.permissions import AllowAny
from django.db.models import Q
from rest_framework import serializers

from .models import Experience, BulletPoint, Media
from rest_framework import viewsets, permissions
from .serializers import ExperienceSerializer, BulletPointsSerializer, MediaSerializer


class ExperienceView(viewsets.ModelViewSet):
    serializer_class = ExperienceSerializer
    queryset = Experience.objects.all()
    permission_classes = (AllowAny,)


class BulletPointsView(viewsets.ModelViewSet):
    serializer_class = BulletPointsSerializer
    queryset = BulletPoint.objects.all()
    permission_classes = (AllowAny,)


class MediaView(viewsets.ModelViewSet):
    serializer_class = MediaSerializer
    queryset = Media.objects.all()
    permission_classes = (AllowAny,)
