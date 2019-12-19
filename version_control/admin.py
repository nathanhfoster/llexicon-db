from django.contrib import admin
from .models import Version
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin


class VersionResource(resources.ModelResource):

    class Meta:
        model = Version
        fields = ('date_created', 'date_updated',)


class VersionAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    resource_class = VersionResource
    list_display = ('date_created', 'date_updated',)


admin.site.register(Version, VersionAdmin)
