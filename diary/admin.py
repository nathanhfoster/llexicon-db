from django.contrib import admin
from .models import Tag, Entry
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin


class TagResource(resources.ModelResource):

    class Meta:
        model = Tag
        import_id_fields = ("title",)
        fields = ('title', 'authors', 'date_created',  'date_updated', )
        widgets = {"authors": {"field": "pk"}}


class TagAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    resource_class = TagResource
    list_display = (
        'title', 'date_created', 'date_updated',)


class EntryResource(resources.ModelResource):

    class Meta:
        model = Entry
        fields = ('id', 'author', 'title', 'html',
                  'date_created', 'date_created_by_author', 'date_updated',
                  'views', 'address', 'latitude', 'longitude', 'is_public', 'tags',)
        widgets = {"tags": {"field": "title"}}


class EntryAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    resource_class = EntryResource
    list_display = (
        'id', 'title', 'author', 'address', 'date_created_by_author', 'date_updated',)


admin.site.register(Entry, EntryAdmin)
admin.site.register(Tag, TagAdmin)
