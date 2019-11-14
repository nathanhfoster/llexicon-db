from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsAuthorOrSuperUser, IsStaffOrTargetUser
from django.db.models import Q
from rest_framework import serializers, pagination
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Entry, Tag
from rest_framework import viewsets, permissions
from .serializers import EntrySerializer, TagSerializer
from django.utils.timezone import now
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
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)


class EntryView(viewsets.ModelViewSet):
    serializer_class = EntrySerializer
    pagination_class = StandardResultsSetPagination
    queryset = Entry.objects.all()
    permission_classes = (IsAuthorOrSuperUser,)

    def get_permissions(self):
        # allow an authenticated user to create via POST
        if self.request.method == 'GET':
            self.permission_classes = (IsAuthorOrSuperUser,)
        if self.request.method == 'PATCH':
            self.permission_classes = (IsAuthorOrSuperUser,)
        if self.request.method == 'POST':
            self.permission_classes = (IsAuthenticated,)
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

        return Response(serializer.data)

    @action(methods=['get'], detail=True, permission_classes=[permission_classes])
    def view(self, request, pk):
        queryset = Entry.objects.all().filter(author=pk)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = EntrySerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = EntrySerializer(queryset, many=True)

        return Response(serializer.data)

    @action(methods=['post'], detail=True, permission_classes=[permission_classes])
    def view_by_date(self, request, pk):

        dateString = request.data['date']
        date = dateString.split('-')
        year = date[0]
        month = date[1]
        day = date[2].split('T')[0]

        # print(year, month, day)

        queryset = Entry.objects.all().filter(
            author=pk,
            date_created_by_author__year__gte=year,
            date_created_by_author__month__gte=month,)
        # end_date__year__lte=year,
        # end_date__month__lte=month, )

        serializer = EntrySerializer(queryset, many=True)

        return Response(serializer.data)
