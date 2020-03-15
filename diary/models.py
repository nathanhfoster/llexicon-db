from django.db import models
from django.conf import settings
from django.utils.timezone import now


class Tag(models.Model):
    authors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='tags', )
    title = models.CharField(max_length=256, primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ('title',)

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
    html = models.TextField(default='<p><br></p>')
    date_created = models.DateTimeField(auto_now_add=True)
    date_created_by_author = models.DateTimeField(default=now())
    date_updated = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    rating = models.PositiveIntegerField(default=0)

    address = models.CharField(max_length=256, blank=True)

    latitude = models.DecimalField(
        max_digits=18, decimal_places=15, blank=True, null=True)
    longitude = models.DecimalField(
        max_digits=18, decimal_places=15, blank=True, null=True)

    is_public = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Entry'
        verbose_name_plural = 'Entries'
        ordering = ('-date_created_by_author', 'date_updated', )

    # def __str__(self):
    #     return self.title
