from rest_framework import serializers, validators
from education.models import Education, Media


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'


class EducationSerializer(serializers.ModelSerializer):
    EducationMedia = MediaSerializer(Media, many=True)

    class Meta:
        model = Education
        fields = ('id',
                  'shcool',
                  'degree',
                  'field_of_study',
                  'start_year',
                  'end_year',
                  'location',
                  'date_created',
                  'grade',
                  'activities_and_societies',
                  'description',
                  'date_created',
                  'EducationMedia',)
