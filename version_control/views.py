from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Version
from rest_framework import viewsets, permissions
from .serializers import VersionSerializer
from dateutil.parser import parse


class VersionView(viewsets.ModelViewSet):
    serializer_class = VersionSerializer
    queryset = Version.objects.all()
    permission_classes = (AllowAny,)

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = (AllowAny,)
        if self.request.method == 'PATCH':
            self.permission_classes = (IsAuthenticated,)
        if self.request.method == 'POST':
            self.permission_classes = (IsAuthenticated,)
        return super(VersionView, self).get_permissions()

    @action(methods=['get'], detail=False, permission_classes=[permission_classes])
    def view(self, request):
        queryset = Version.objects.latest('date_created')
        serializer = VersionSerializer(queryset)

        return Response(serializer.data)

    @action(methods=['post'], detail=False, permission_classes=[permission_classes])
    def latest(self, request):
        clientVersion = parse(request.data['version'])
        try:
            queryset = Version.objects.latest('date_created')
            latestVersion = parse(getattr(queryset, 'date_created'))
            print('latestVersion: ', latestVersion)
            print("clientVersion: ", clientVersion)
            if clientVersion < latestVersion:
                clientVersion = latestVersion
        except:
            pass

        return Response(clientVersion)
