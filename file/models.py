from django.db import models
from diary.models import Entry


class File(models.Model):
    TYPES = (
        ('Image', 'Image'),
        ('Video', 'Video'),
        ('File', 'File'),
    )
    entry_id = models.ForeignKey(
        Entry,
        related_name='EntryFiles',
        on_delete=models.CASCADE, )
    media_type = models.CharField(blank=True, max_length=6, choices=TYPES)
    url = models.FileField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'File'
        verbose_name_plural = 'Files'
        ordering = ('-date_created',)
