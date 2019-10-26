from django.db import models
from django.conf import settings


class Experience(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='UserExperience',
        on_delete=models.CASCADE, )
    title = models.CharField(max_length=256)
    company = models.CharField(max_length=256)
    location = models.CharField(max_length=256)
    start_date = models.CharField(max_length=8)
    end_date = models.CharField(max_length=8)

    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Experience'
        verbose_name_plural = 'Experiences'
        ordering = ('-start_date',)
        # unique_together = ('provider_id',)

    def __str__(self):
        return self.title

    @property
    def get_title(self):
        return self.title


class BulletPoint(models.Model):
    experience_id = models.ForeignKey(
        Experience,
        related_name='BulletPoint',
        null=True,
        on_delete=models.CASCADE,)

    title = models.CharField(max_length=256)
    position = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'BulletPoint'
        verbose_name_plural = 'BulletPoint'
        ordering = ('position',)
        # unique_together = ('experience_id', 'follower',)


class Media(models.Model):
    experience_id = models.ForeignKey(
        Experience,
        related_name='ExperienceMedia',
        on_delete=models.CASCADE,)
    title = models.CharField(max_length=256)
    description = models.TextField()
    link = models.CharField(max_length=512)
    position = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Media'
        verbose_name_plural = 'Medias'
        ordering = ('position',)
