from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from .views import CustomAuthToken

urlpatterns = [
    path('', admin.site.urls),
    path('api/v1/', include('authentication_authorization.urls')),
    path('api/v1/', include('user.urls')),
    path('api/v1/', include('experience.urls')),
    path('api/v1/', include('education.urls')),
    path('api/v1/', include('technical_skill.urls')),
    path('api/v1/', include('social_authentication.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/login/', CustomAuthToken.as_view())
]

# if settings.DEBUG:
# Serve static and media files from development server
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
