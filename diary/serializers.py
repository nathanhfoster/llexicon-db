from rest_framework import serializers, validators
from .models import Entry, Tag, Person
from file.models import File
from file.serializers import FileSerializer

class TagMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)

class PersonMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('name',)


class EntrySerializer(serializers.ModelSerializer):
    tags = TagMinimalSerializer(Tag, many=True,  read_only=True, required=False)
    people = PersonMinimalSerializer(Person, many=True,  read_only=True, required=False)
    EntryFiles = FileSerializer(
        File, many=True,  read_only=True, required=False)

    class Meta:
        model = Entry
        fields = '__all__'

class EntryMinimalSerializer(serializers.ModelSerializer):
    tags = TagMinimalSerializer(Tag, many=True,  read_only=True, required=False)
    people = PersonMinimalSerializer(Person, many=True,  read_only=True, required=False)
    EntryFiles = FileSerializer(
        File, many=True,  read_only=True, required=False)

    class Meta:
        model = Entry
        fields = '__all__'
