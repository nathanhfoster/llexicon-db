from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsAuthorOrSuperUser, IsStaffOrTargetUser
from django.db.models import F, Q
from rest_framework import serializers, pagination
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Entry, Tag, Person
from rest_framework import viewsets, permissions
from .serializers import AdminEntrySerializer, EntrySerializer, EntryMinimalSerializer, EntryProtectedSerializer, TagMinimalSerializer, PersonMinimalSerializer
from django.utils.timezone import now
import json
from rest_framework.filters import SearchFilter
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from django.shortcuts import get_object_or_404


class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    # max_page_size = 250


class LargeResultsSetPagination(pagination.PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    # max_page_size = 1000


class TagView(viewsets.ModelViewSet):
    serializer_class = TagMinimalSerializer
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


class PersonView(viewsets.ModelViewSet):
    serializer_class = PersonMinimalSerializer
    queryset = Person.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        if self.request.method == 'GET':
            if self.request.path.find('view') != -1:
                self.permission_classes = (IsAuthenticated,)
        if self.request.method == 'PATCH':
            self.permission_classes = (IsAuthenticated,)
        if self.request.method == 'POST':
            self.permission_classes = (IsAuthenticated,)
        return super(PersonView, self).get_permissions()

    @action(methods=['get'], detail=True, permission_classes=[permission_classes])
    def view(self, request, pk):
        queryset = Person.objects.all().filter(authors=pk)

        serializer = PersonMinimalSerializer(queryset, many=True)

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
            # if self.request.path.find('update_entry') != -1:
            #     self.permission_classes = (IsAuthenticated,)
            # else:
            self.permission_classes = (IsAuthorOrSuperUser,)
        if self.request.method == 'POST':
            if self.request.path.find('public_view') != -1:
                self.permission_classes = (AllowAny,)
            else:
                self.permission_classes = (IsAuthenticated,)
        return super(EntryView, self).get_permissions()

    @action(methods=['patch'], detail=True, permission_classes=[permission_classes])
    def update_entry(self, request, pk):
        entry = get_object_or_404(Entry, id=pk)
        user = request.user

        for key in request.data:
            if key == 'tags':
                entry.tags.clear()
                tags = request.data[key].split(',')
                for tagName in tags:
                    if (tagName):
                        tag, tagCreate = Tag.objects.get_or_create(
                            name=tagName)
                        tag.authors.add(user)
                        entry.tags.add(tag)
            elif key == 'people':
                entry.people.clear()
                # tags = json.loads(request.data[key])
                people = request.data[key].split(',')
                for personName in people:
                    # tagName = t['title']
                    if (personName):
                        person, personCreate = Person.objects.get_or_create(
                            name=personName)
                        person.authors.add(user)
                        entry.people.add(person)

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

    @action(methods=['get'], detail=False, permission_classes=[permission_classes])
    def all(self, request):
        queryset = Entry.objects.all()
        serializer = AdminEntrySerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True, permission_classes=[permission_classes])
    def view(self, request, pk):
        queryset = Entry.objects.all().filter(author=pk)

        serializer = EntryMinimalSerializer(queryset, many=True)

        return Response(serializer.data)

    @action(methods=['get'], detail=True, permission_classes=[permission_classes])
    def details(self, request, pk):
        user = request.user
        entry = get_object_or_404(Entry, pk=pk)
        Entry.objects.all().filter(pk=pk).update(views=F('views') + 1)
        entry.refresh_from_db()
       # entry.views += 1
       # entry.save()
        serializer = EntryProtectedSerializer(entry) if(
            user.is_anonymous) else EntryMinimalSerializer(entry)

        return Response(serializer.data)

    @action(methods=['post'], detail=True, permission_classes=[permission_classes])
    def public_view(self, request, pk):
        author = pk
        entries = Entry.objects.all().filter(author=author, is_public=True)

        serializer = EntryMinimalSerializer(entries, many=True)

        return Response(serializer.data)

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

        # dateString = request.data['date']
        # date = dateString.split('-')
        # year = date[0]
        # month = date[1]
        # day = date[2].split('T')[0]

        year = request.data['year'] if 'year' in request.data else None
        month = request.data['month'] if 'month' in request.data else None
        day = request.data['day'] if 'day' in request.data else None

        # print(year, month, day)

        queryset = None
        if(year and month and day):
            queryset = Entry.objects.all().filter(
                author=pk,
                date_created_by_author__year__gte=year,
                date_created_by_author__month__gte=month,
                date_created_by_author__day__gte=day,)
        elif (year and day):
            queryset = Entry.objects.all().filter(
                author=pk,
                date_created_by_author__year__gte=year,
                date_created_by_author__day__gte=day,)

        elif (month and day):
            queryset = Entry.objects.all().filter(
                author=pk,
                date_created_by_author__month__gte=month,
                date_created_by_author__day__gte=day,)

        elif (year):
            queryset = Entry.objects.all().filter(
                author=pk, date_created_by_author__year__gte=year,)

        elif (month):
            queryset = Entry.objects.all().filter(
                author=pk, date_created_by_author__month__gte=month,)

        elif (day):
            queryset = Entry.objects.all().filter(
                author=pk, date_created_by_author__day__gte=day,)
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
            Q(tags__name__icontains=s) |
            Q(people__name__icontains=s) |
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
