from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User, Setting
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User


class SettingResource(resources.ModelResource):

    class Meta:
        model = Setting
        fields = ('id', 'user', 'show_footer', 'full_container_width',
                  'push_messages', 'offline_mode',)


class SettingAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    resource_class = SettingResource
    list_display = (
        'user', 'show_footer', 'full_container_width', 'push_messages', 'offline_mode',)


class UserResource(resources.ModelResource):

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'is_superuser', 'is_staff',  'is_active', 'date_joined', 'last_login',
                  'facebook_id', 'google_id', 'picture',
                  'uploaded_picture', 'opt_in',)


class UserAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    resource_class = UserResource
    list_display = (
        'username', 'id', 'opt_in',
        'is_superuser', 'email', 'is_staff',
        'is_active', 'date_joined', 'last_login',)


admin.site.register(User, UserAdmin)
admin.site.register(Setting, SettingAdmin)
