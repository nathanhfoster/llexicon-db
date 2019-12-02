from django.contrib import admin
from .models import Entry, Tag

class CustomEntry(admin.ModelAdmin):
    model = Entry
    list_display = (
        'id', 'title', 'author', 'date_created_by_author', 'date_updated',)

class CustomTag(admin.ModelAdmin):
    model = Tag
    list_display = (
        'title', 'date_created', 'date_updated',)


admin.site.register(Entry, CustomEntry)
admin.site.register(Tag, CustomTag)
