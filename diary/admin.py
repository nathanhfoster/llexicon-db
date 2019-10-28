from django.contrib import admin
from .models import Entry, Tag

admin.site.register(Entry)
admin.site.register(Tag)