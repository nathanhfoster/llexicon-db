from django.db import models


class Version(models.Model):
    date_created = models.DateTimeField(auto_now_add=True, primary_key=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Version'
        verbose_name_plural = 'Versions'
        ordering = ('-date_created',)
