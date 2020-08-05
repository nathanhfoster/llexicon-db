from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# Allow Spaces in User names


class MyValidator(UnicodeUsernameValidator):
    regex = r'^[\w.@+\- ]+$'


class Setting(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='Settings',
        on_delete=models.CASCADE,)

    show_animated_background = models.BooleanField(default=True)
    push_messages = models.BooleanField(default=False)
    offline_mode = models.BooleanField(default=False)
    dark_mode = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Setting'
        verbose_name_plural = 'Settings'
        ordering = ('-user',)


class User(AbstractUser):
    facebook_id = models.CharField(blank=True, max_length=256)
    google_id = models.CharField(blank=True, max_length=256)
    picture = models.TextField(blank=True)
    uploaded_picture = models.ImageField(blank=True, null=True)
    username_validator = MyValidator()
    username = models.CharField(
        ('username'),
        max_length=150,
        unique=True,
        help_text=(
            'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': ("A user with that username or email already exists."),
        },
    )
    email = models.EmailField(unique=True)
    opt_in = models.BooleanField(blank=True, default=False)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ('-username',)
        unique_together = ('email',)

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)
            Setting.objects.create(user=instance)
    pass

    @property
    def get_picture(self):
        return self.picture
