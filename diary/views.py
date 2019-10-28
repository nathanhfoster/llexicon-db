from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Entry, Tag
from rest_framework import viewsets, permissions
from .serializers import EntrySerializer, TagSerializer

class TagView(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)

class EntryView(viewsets.ModelViewSet):
    serializer_class = EntrySerializer
    queryset = Entry.objects.all()
    permission_classes = (AllowAny,)

    def get_permissions(self):
        # allow an authenticated user to create via POST
        if self.request.method == 'GET':
            self.permission_classes = (IsAuthenticated,)
        if self.request.method == 'PATCH':
            self.permission_classes = (
                IsAuthenticated,)
        return super(EntryView, self).get_permissions()

    @action(methods=['get'], detail=True, permission_classes=[permission_classes])
    def view(self, request, pk):
        queryset = Entry.objects.all().filter(author=pk)

        serializer = EntrySerializer(queryset, many=True)

        return Response(serializer.data)

