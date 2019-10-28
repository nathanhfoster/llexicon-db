from rest_framework import serializers, validators
from .models import Entry, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class EntrySerializer(serializers.ModelSerializer):
    tags = TagSerializer(Tag, many=True)
    class Meta:
        model = Entry
        fields = '__all__'
