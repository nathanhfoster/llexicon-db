from django.contrib import admin
from .models import SocialAuthentication

class CustomSocialAuthentication(admin.ModelAdmin):
    model = SocialAuthentication
    list_display = (
        'id', 'provider', 'user', 
        'name', 'email',)

admin.site.register(SocialAuthentication, CustomSocialAuthentication)
