from rest_framework import serializers, validators
from .models import Version


class VersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = '__all__'
