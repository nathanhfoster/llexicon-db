from rest_framework import serializers, validators
from experience.models import Experience, BulletPoint, Media


class BulletPointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BulletPoint
        fields = '__all__'


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'


class ExperienceSerializer(serializers.ModelSerializer):
    BulletPoint = BulletPointsSerializer(BulletPoint, many=True)
    ExperienceMedia = MediaSerializer(Media, many=True)

    class Meta:
        model = Experience
        fields = ('id',
                  'title',
                  'company',
                  'location',
                  'start_date',
                  'end_date',
                  'description',
                  'date_created',
                  'BulletPoint',
                  'ExperienceMedia',)
