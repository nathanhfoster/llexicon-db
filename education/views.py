from rest_framework.permissions import AllowAny
from django.db.models import Q
from rest_framework import serializers

from .models import Education, Media
from rest_framework import viewsets, permissions
from .serializers import EducationSerializer, MediaSerializer


class EducationView(viewsets.ModelViewSet):
    serializer_class = EducationSerializer
    queryset = Education.objects.all()
    permission_classes = (AllowAny,)


class MediaView(viewsets.ModelViewSet):
    serializer_class = MediaSerializer
    queryset = Media.objects.all()
    permission_classes = (AllowAny,)
