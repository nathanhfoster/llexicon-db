from django.db import models
from django.conf import settings


class SocialAuthentication(models.Model):
    provider = models.CharField(max_length=256)
    provider_id = models.CharField(max_length=256)
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='SocialAuthentication',
        on_delete=models.CASCADE, )
    access_token = models.TextField()
    expires_in = models.CharField(max_length=256)
    expires_at = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    picture = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Social Provider'
        verbose_name_plural = 'Social Providers'
        ordering = ('-user_id',)
        unique_together = ('provider_id',)
