from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsAuthorOrSuperUser, IsStaffOrTargetUser
from django.db.models import Q
from rest_framework import serializers, pagination
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework import viewsets, permissions
from .models import File
from .serializers import FileSerializer
import json


class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 500


class LargeResultsSetPagination(pagination.PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 1000


class TagView(viewsets.ModelViewSet):
    serializer_class = FileSerializer
    queryset = File.objects.all()
    permission_classes = (AllowAny,)


class FileView(viewsets.ModelViewSet):
    serializer_class = FileSerializer
    pagination_class = StandardResultsSetPagination
    queryset = File.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = (IsAuthenticated,)
        if self.request.method == 'PATCH':
            self.permission_classes = (IsAuthenticated,)
        return super(FileView, self).get_permissions()

    @action(methods=['get'], detail=True, permission_classes=[permission_classes])
    def view(self, request, pk):
        queryset = File.objects.all().filter(entry_id=pk)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = FileSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = FileSerializer(queryset, many=True)

        return Response(serializer.data)
