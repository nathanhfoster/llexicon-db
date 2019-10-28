from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Entry, Tag
from rest_framework import viewsets, permissions
from .serializers import EntrySerializer, TagSerializer
from django.utils.timezone import now
import json


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

    @action(methods=['patch'], detail=True, permission_classes=[permission_classes])
    def update_with_tags(self, request, pk):
        entry = Entry.objects.get(id=pk)

        for key in request.data:
            if key == 'tags':
                tags = json.loads(request.data[key])
                entry.tags.clear()
                entry.tags.set(tags)
            else:
                value = request.data[key]
                setattr(entry, key, value)

        entry.date_updated = now()
        entry.save()
        serializer = EntrySerializer(entry)

        # try:
        #     entry.tags.set(tags)
        # except:
        #     for i in tags:
        #         t = Tag.objects.get(id=i)
        #         t.entry_set.add(pk)
        # return Response(json.dumps(tags))
        return Response(serializer.data)

    @action(methods=['get'], detail=True, permission_classes=[permission_classes])
    def view(self, request, pk):
        queryset = Entry.objects.all().filter(author=pk)

        serializer = EntrySerializer(queryset, many=True)

        return Response(serializer.data)
