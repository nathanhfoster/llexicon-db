from rest_framework import serializers, validators
from .models import Entry, Tag
from file.models import File
from file.serializers import FileSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class EntrySerializer(serializers.ModelSerializer):
    tags = TagSerializer(Tag, many=True,  read_only=True, required=False)
    EntryFiles = FileSerializer(
        File, many=True,  read_only=True, required=False)

    class Meta:
        model = Entry
        fields = '__all__'
