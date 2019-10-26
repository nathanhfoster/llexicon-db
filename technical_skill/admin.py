from django.contrib import admin
from .models import Specialization, Skill, SpecializationSkillExperience

admin.site.register(Specialization)
admin.site.register(Skill)
admin.site.register(SpecializationSkillExperience)
