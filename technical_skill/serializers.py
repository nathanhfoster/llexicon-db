from rest_framework import serializers, validators
from technical_skill.models import Specialization, Skill, SpecializationSkillExperience


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = '__all__'


class SpecializationMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = ('title',)


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'


class SkillMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('title',)


class SpecializationSkillExperienceSerializer(serializers.ModelSerializer):
    specialization = SpecializationMinimalSerializer(Specialization)
    skills = SkillMinimalSerializer(Skill, many=True)

    class Meta:
        model = SpecializationSkillExperience
        fields = '__all__'
