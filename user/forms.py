from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = (
            'username', 'id', 'opt_in',
            'is_superuser', 'email', 'is_staff',
            'is_active', 'date_joined', 'last_login', )


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = (
            'username', 'opt_in',
            'is_superuser', 'email', 'is_staff',
            'is_active', 'date_joined', 'last_login', )
