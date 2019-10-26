from django.db import models
from django.conf import settings


class Education(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='UserEducation',
        on_delete=models.CASCADE, )
    shcool = models.CharField(max_length=256)
    degree = models.CharField(max_length=256)
    field_of_study = models.CharField(max_length=256)
    start_year = models.IntegerField()
    end_year = models.IntegerField()
    location = models.CharField(max_length=256)
    date_created = models.DateTimeField(auto_now_add=True)
    grade = models.FloatField()
    activities_and_societies = models.TextField()
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Education'
        verbose_name_plural = 'Educations'
        ordering = ('-end_year',)

    def __str__(self):
        return self.shcool

    @property
    def get_school(self):
        return self.shcool


class Media(models.Model):
    education_id = models.ForeignKey(
        Education,
        related_name='EducationMedia',
        on_delete=models.CASCADE,)
    title = models.CharField(max_length=256)
    link = models.CharField(max_length=512)
    position = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Media'
        verbose_name_plural = 'Medias'
        ordering = ('-date_created',)
