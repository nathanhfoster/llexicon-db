from django.contrib import admin
from .models import Tag, Person, Entry
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin


class TagResource(resources.ModelResource):

    class Meta:
        model = Tag
        import_id_fields = ("name",)
        fields = ('name', 'authors', 'date_created',  'date_updated', )
        widgets = {"authors": {"field": "pk"}}


class TagAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    resource_class = TagResource
    list_display = ('name', 'date_created', 'date_updated',)
    search_fields = ('name', 'date_created',  'date_updated', )


class PersonResource(resources.ModelResource):

    class Meta:
        model = Person
        import_id_fields = ("name",)
        fields = ('name', 'authors', 'date_created',  'date_updated', )
        widgets = {"authors": {"field": "pk"}}


class PersonAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    resource_class = PersonResource
    list_display = ('name', 'date_created', 'date_updated',)
    search_fields = ('name', 'date_created',  'date_updated', )


class EntryResource(resources.ModelResource):

    class Meta:
        model = Entry
        fields = ('id', 'author', 'title', 'html',
                  'date_created', 'date_created_by_author', 'date_updated',
                  'views', 'rating', 'address', 'latitude', 'longitude', 'is_public', 'tags', 'people',)
        widgets = {"tags": {"field": "name"}, "people": {"field": "name"}}


class EntryAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    resource_class = EntryResource

    list_display = (
        'id', 'title', 'author', 'address', 'views', 'rating', 'is_public', 'date_created_by_author', 'date_updated',)

    search_fields = ('title', 'address', 'views', 'rating',
                     'is_public', 'date_created_by_author', 'date_updated',)
    # autocomplete_fields = ('author', )


admin.site.register(Entry, EntryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Person, PersonAdmin)
