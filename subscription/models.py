from django.db import models
from django.utils.timezone import now


class Subscription(models.Model):
    id = models.TextField(primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_modified = models.DateTimeField(default=now)

    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
        ordering = ('-date_created',)
