from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.conf import settings
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from django.contrib.auth.models import update_last_login


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        update_last_login(None, user)
        token, created = Token.objects.get_or_create(user=user)
        print(user.uploaded_picture)
        uploaded_picture = None
        try:
            uploaded_picture = user.uploaded_picture.url
        except: pass
        return Response({
            'token': token.key,
            'id': user.pk,
            'facebook_id': user.facebook_id,
            'google_id': user.google_id,
            'picture': user.picture,
            'uploaded_picture': uploaded_picture,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_active': user.is_active,
            'last_login': user.last_login,
            'opt_in': user.opt_in,
            'date_joined': user.date_joined,
            'location': user.location,
            'profile_uri': user.profile_uri
        })