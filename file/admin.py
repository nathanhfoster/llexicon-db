from django.contrib import admin
from .models import File


class CustomFile(admin.ModelAdmin):
    model = File
    list_display = (
        'id', 'author', 'media_type', 'url',
        'date_created', 'date_updated',)


admin.site.register(File, CustomFile)
