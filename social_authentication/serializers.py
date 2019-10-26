from rest_framework import serializers, validators
from social_authentication.models import SocialAuthentication


class SocialAuthenticationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialAuthentication
        fields = '__all__'
