from django.contrib import admin
from .models import File
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin


class CustomFile(admin.ModelAdmin):
    model = File


class FileResource(resources.ModelResource):

    class Meta:
        model = File
        fields = ('id', 'entry_id', 'media_type', 'url',
                  'date_created', 'date_updated',)


class FileAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    resource_class = FileResource
    list_display = (
        'id', 'entry_id', 'media_type', 'url',
        'date_created', 'date_updated',)


admin.site.register(File, FileAdmin)
