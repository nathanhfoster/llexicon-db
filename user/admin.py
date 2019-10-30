from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User, Setting


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = (
        'username', 'id', 'opt_in',
        'is_superuser', 'email', 'is_staff',
        'is_active', 'date_joined', 'last_login',)


admin.site.register(User, CustomUserAdmin)
admin.site.register(Setting)
