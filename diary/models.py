from django.db import models
from django.conf import settings
from django.utils.timezone import now

class Tag(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='tags',
        on_delete=models.CASCADE, )
    title = models.CharField(max_length=256)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ('-date_created',)

    def __str__(self):
        return self.title

class Entry(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='entires',
        on_delete=models.CASCADE, )
    tags = models.ManyToManyField(
        Tag,
        related_name='tags',
        blank=True, )
    title = models.CharField(max_length=256, blank=True)
    html = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_created_by_author = models.DateTimeField(default=now())
    date_updated = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    

    class Meta:
        verbose_name = 'Entry'
        verbose_name_plural = 'Entries'
        ordering = ('-date_created',)

    # def __str__(self):
    #     return self.title