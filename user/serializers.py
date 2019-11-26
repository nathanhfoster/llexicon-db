from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from user.models import User, Setting
from social_authentication.models import SocialAuthentication
from social_authentication.serializers import SocialAuthenticationSerializer


class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = ('id', 'user', 'show_footer',
                  'push_messages', 'offline_mode',)
        read_only_fields = ('id',)


class SettingViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        exclude = ('id', 'user',)
        read_only_fields = ('id',)


class UserSerializer(serializers.ModelSerializer):
    SocialAuthentications = SocialAuthenticationSerializer(
        SocialAuthentication, many=True, read_only=True)
    Settings = SettingSerializer(Setting, read_only=True)

    class Meta:
        model = User
        fields = '__all__'
        write_only_fields = ('password',)
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('date_joined',)

    def create(self, validated_data):
        user = None
        try:
            user = User.objects.create(
                email=validated_data['email'],
                username=validated_data['username'],
                password=make_password(validated_data['password']),
                opt_in=validated_data['opt_in'],
                picture=validated_data['picture'],
            )
        # Social Login
        except:
            user = User.objects.create(
                email=validated_data['email'],
                username=validated_data['username'],
                password=make_password(validated_data['password']),
                opt_in=validated_data['opt_in']
            )

        user.set_password(validated_data["password"])
        user.save()
        return user

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


class AllUserSerializer(serializers.ModelSerializer):
    SocialAuthentications = SocialAuthenticationSerializer(
        SocialAuthentication, many=True)
    Settings = SettingSerializer(Setting)

    class Meta:
        model = User
        fields = (
            'id',
            'facebook_id',
            'google_id',
            'picture',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_superuser',
            'is_staff',
            'is_active',
            'last_login',
            'bio',
            'opt_in',
            'date_joined',
            'SocialAuthentications',
            'groups',
            'user_permissions',
            'Settings', )
        write_only_fields = ('password',)
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('date_joined', )


class Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'groups', 'user_permissions',
            'is_active', 'last_login',
        )


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'groups', 'user_permissions', 'username', 'first_name', 'last_name', 'opt_in', 'last_login',
            'is_superuser', 'email', 'is_staff',
            'is_active', 'date_joined', 'last_login',
        )
