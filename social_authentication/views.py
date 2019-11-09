from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q
from rest_framework import serializers

from .models import SocialAuthentication
from rest_framework import viewsets, permissions
from .serializers import SocialAuthenticationSerializer
from user.permissions import IsAuthorOrSuperUser, IsStaffOrTargetUser
from rest_framework.decorators import action
from rest_framework.response import Response
from user.models import User
from user.serializers import UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.models import update_last_login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import update_last_login


class SocialAuthenticationView(viewsets.ModelViewSet):
    serializer_class = SocialAuthenticationSerializer
    queryset = SocialAuthentication.objects.all()
    permission_classes = (AllowAny,)

    def get_permissions(self):
        # allow an authenticated user to create via POST
        if self.request.method == 'GET':
            self.permission_classes = (AllowAny,)
        if self.request.method == 'POST':
            self.permission_classes = (AllowAny,)
        if self.request.method == 'PATCH':
            self.permission_classes = (
                IsAuthenticated,)
        return super(SocialAuthenticationView, self).get_permissions()

    @action(methods=['post'], detail=True, permission_classes=[permission_classes])
    def provider(self, request, pk):
        providerIsFacebook = request.data['provider'] == "Facebook"

        name = request.data['name']
        password = make_password(pk)
        email = request.data['email']
        picture = request.data['picture']
        [first_name, last_name] = str.split(name)

        username = name.replace(" ", "")

        user, userCreated = User.objects.filter(
            Q(email=email)
            | Q(facebook_id=pk)
            | Q(google_id=pk),
        ).get_or_create(
            email=email,

            defaults={
                'facebook_id': pk,
                'username': username,
                'password': password,
                'first_name': first_name,
                'last_name': last_name,
                'picture': picture
            } if(providerIsFacebook) else {
                'google_id': pk,
                'username': username,
                'password': password,
                'first_name': first_name,
                'last_name': last_name,
                'picture': picture
            },
        )

        if user:
            # record already exist
            setattr(user, 'first_name', first_name)
            setattr(user, 'last_name', last_name)
            if(not getattr(user, 'picture')):
                setattr(user, 'picture', picture)
            if(providerIsFacebook):
                setattr(user, 'facebook_id', pk)
            else:
                setattr(user, 'google_id', pk)

        # if userCreated:
            # update record with defaults

        user.save()
        userSerialized = UserSerializer(user)
        update_last_login(None, user)

        token, created = Token.objects.get_or_create(user=user)

        socialAuthentication, socialAuthCreated = SocialAuthentication.objects.get_or_create(
            provider_id=pk,
            defaults={
                'provider': request.data['provider'],
                'user': user,
                'access_token': request.data['access_token'],
                'expires_in': request.data['expires_in'],
                'expires_at': request.data['expires_at'],
                'name': name,
                'email': email,
                'picture': picture
            },
        )
        return Response({**{'token': token.key}, **userSerialized.data})
