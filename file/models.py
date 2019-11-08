from django.db import models
from django.conf import settings


class File(models.Model):
    TYPES = (
        ('Image', 'Image'),
        ('Video', 'Video'),
        ('File', 'File'),
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='UserMedia',
        on_delete=models.CASCADE,
        blank=True, null=True, )
    media_type = models.CharField(blank=True, max_length=6, choices=TYPES)
    url = models.FileField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'File'
        verbose_name_plural = 'Files'
        ordering = ('-date_created',)
