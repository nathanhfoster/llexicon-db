from django.db import models
from django.conf import settings


class Specialization(models.Model):
    title = models.CharField(max_length=256, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Specialization'
        verbose_name_plural = 'Specializations'
        ordering = ('title',)

    def __str__(self):
        return self.title


class Skill(models.Model):
    title = models.CharField(max_length=256, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'
        ordering = ('title',)

    def __str__(self):
        return self.title


class SpecializationSkillExperience(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='UserSpecialization',
        on_delete=models.CASCADE, )
    specialization = models.ForeignKey(
        Specialization,
        related_name='SpecializationSkillExperience',
        on_delete=models.CASCADE,)
    skills = models.ManyToManyField(
        Skill, blank=True, verbose_name="Specialization Skills")

    position = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)

    def title(self):
        return self.specialization. get_title()

    class Meta:
        verbose_name = 'SpecializationSkillExperience'
        verbose_name_plural = 'SpecializationSkillExperiences'
        ordering = ('position',)
