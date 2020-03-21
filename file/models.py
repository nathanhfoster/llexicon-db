from django.db import models
from diary.models import Entry
from django.utils.timezone import now


class File(models.Model):
    # TYPES = (
    #     ('Image', 'Image'),
    #     ('Video', 'Video'),
    #     ('File', 'File'),
    # )
    # choices=TYPES

    entry_id = models.ForeignKey(
        Entry,
        related_name='EntryFiles',
        on_delete=models.CASCADE, )
    file_type = models.CharField(blank=True, max_length=24)
    name = models.CharField(blank=True, max_length=512)
    size = models.IntegerField(default=0)
    url = models.FileField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_modified = models.DateTimeField(default=now)

    class Meta:
        verbose_name = 'File'
        verbose_name_plural = 'Files'
        ordering = ('-date_created',)
