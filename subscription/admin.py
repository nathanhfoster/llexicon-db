from django.contrib import admin
from .models import Subscription
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin


class SubscriptionResource(resources.ModelResource):

    class Meta:
        model = Subscription
        fields = ('id',
                  'date_created', 'date_updated', 'date_modified',)


class SubscriptionAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    resource_class = SubscriptionResource
    list_display = ('id',
                    'date_created', 'date_updated', 'date_modified',)
    search_fields = ('id',
                     'date_created', 'date_updated', 'date_modified',)


admin.site.register(Subscription, SubscriptionAdmin)
