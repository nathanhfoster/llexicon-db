from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q
from rest_framework import serializers, pagination
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework import viewsets, permissions
from .models import Subscription
from .serializers import SubscriptionSerializer


class SubscriptionView(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = (IsAuthenticated,)
        if self.request.method == 'PATCH':
            self.permission_classes = (IsAuthenticated,)
        return super(SubscriptionView, self).get_permissions()

