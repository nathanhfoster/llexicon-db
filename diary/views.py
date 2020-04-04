from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsAuthorOrSuperUser, IsStaffOrTargetUser
from django.db.models import F, Q
from rest_framework import serializers, pagination
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Entry, Tag
from rest_framework import viewsets, permissions
from .serializers import EntrySerializer, EntryMinimalSerializer, TagSerializer, TagMinimalSerializer
from django.utils.timezone import now
import json
from rest_framework.filters import SearchFilter
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from django.shortcuts import get_object_or_404


class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    # max_page_size = 500


class LargeResultsSetPagination(pagination.PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    # max_page_size = 1000


class TagView(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        if self.request.method == 'GET':
            if self.request.path.find('view') != -1:
                self.permission_classes = (IsAuthenticated,)
        if self.request.method == 'PATCH':
            self.permission_classes = (IsAuthenticated,)
        if self.request.method == 'POST':
            self.permission_classes = (IsAuthenticated,)
        return super(TagView, self).get_permissions()

    @action(methods=['get'], detail=True, permission_classes=[permission_classes])
    def view(self, request, pk):
        queryset = Tag.objects.all().filter(authors=pk)

        serializer = TagMinimalSerializer(queryset, many=True)

        return Response(serializer.data)


class EntryView(viewsets.ModelViewSet):
    serializer_class = EntrySerializer
    pagination_class = StandardResultsSetPagination
    queryset = Entry.objects.all()
    permission_classes = (IsAuthorOrSuperUser,)
    filter_backends = (SearchFilter, )
    search_fields = ('title', 'html', 'address')

    def get_permissions(self):
        if self.request.method == 'GET':
            if self.request.path.find('view') != -1 or self.request.path.find('page') != -1:
                self.permission_classes = (IsAuthenticated,)
            else:
                self.permission_classes = (IsAuthorOrSuperUser,)
        if self.request.method == 'PATCH':
            # if self.request.path.find('update_with_tags') != -1:
            #     self.permission_classes = (IsAuthenticated,)
            # else:
            self.permission_classes = (IsAuthorOrSuperUser,)
        if self.request.method == 'POST':
            self.permission_classes = (IsAuthenticated,)
        return super(EntryView, self).get_permissions()

    @action(methods=['patch'], detail=True, permission_classes=[permission_classes])
    def update_with_tags(self, request, pk):
        entry = get_object_or_404(Entry, id=pk)
        user = request.user

        for key in request.data:
            if key == 'tags':
                entry.tags.clear()
                # tags = json.loads(request.data[key])
                tags = request.data[key].split(',')
                for tagTitle in tags:
                    # tagTitle = t['title']
                    if (tagTitle):
                        tag, tagCreate = Tag.objects.get_or_create(title=tagTitle)
                        tag.authors.add(user)
                        entry.tags.add(tag)

            else:
                value = request.data[key]

                if(value == 'true'):
                    value = True
                elif value == 'false':
                    value = False

                setattr(entry, key, value)

        entry.save()
        serializer = EntrySerializer(entry)

        return Response(serializer.data)

    @action(methods=['get'], detail=True, permission_classes=[permission_classes])
    def view(self, request, pk):
        queryset = Entry.objects.all().filter(author=pk)

        serializer = EntryMinimalSerializer(queryset, many=True)

        return Response(serializer.data)

    @action(methods=['get'], detail=True, permission_classes=[permission_classes])
    def details(self, request, pk):
        # user = request.user
        entry = get_object_or_404(Entry, pk=pk)
        entry.views += 1
        entry.save()
        queryset = entry
        serializer = EntryMinimalSerializer(queryset)
        response = serializer.data
        return Response(response)

    @action(methods=['get'], detail=True, permission_classes=[permission_classes])
    def page(self, request, pk):
        queryset = Entry.objects.all().filter(author=pk)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = EntryMinimalSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = EntryMinimalSerializer(queryset, many=True)

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

        serializer = EntryMinimalSerializer(queryset, many=True)

        return Response(serializer.data)

    @action(methods=['post'], detail=True, permission_classes=[permission_classes])
    def search(self, request, pk):

        s = request.data['search']

        if len(s) < 2:
            return Response([])

        # query = SearchQuery(s)

        # searchVector = SearchVector('title', 'html', 'address', 'tags', )

        # vector = SearchVector('tags', weight='A') + SearchVector('title', weight='B') + SearchVector('html', weight='B') + SearchVector('address', weight='B')

        # searchRank=SearchRank(vector, query)

        # queryset = Entry.objects.annotate(rank=searchRank).filter(Q(author=pk)).order_by('rank')

        queryset = Entry.objects.all().filter(
            Q(author=pk),
            Q(tags__in=s) |
            Q(title__icontains=s) |
            Q(html__icontains=s) |
            Q(address__icontains=s)
        )

        serializer = EntryMinimalSerializer(queryset, many=True)

        # print("QUERY: ", queryset)

        return Response(serializer.data)

    @action(methods=['post'], detail=False, permission_classes=[permission_classes])
    def sync(self, request):
        user = request.user
        entries = Entry.objects.all()
        entryIdsFromClient = json.loads(request.data.get('entries'))
        entriesToGet = []
        entriesToDelete = []

        # print('entryIdsFromClient: ', entryIdsFromClient)

        for e in entries:
            try:
                index = entryIdsFromClient.index(e.id)
                entryIdsFromClient.remove(index)
            except:
                entriesToGet.append(e.id)
                # continue

        response = json.dumps(entryIdsFromClient)
        # print('entriesToDelete: ', entriesToDelete)

        return Response(response)
