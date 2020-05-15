from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from .views import CustomAuthToken

# from rest_auth.views import (
#     LoginView, LogoutView, UserDetailsView, PasswordChangeView,
#     PasswordResetView, PasswordResetConfirmView
# )

urlpatterns = [
    path('', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('api/v1/', include('authentication_authorization.urls')),
    path('api/v1/', include('user.urls')),
    path('api/v1/', include('diary.urls')),
    path('api/v1/', include('social_authentication.urls')),
    path('api/v1/', include('file.urls')),
    path('api/v1/api-auth/', include('rest_framework.urls')),
    path('api/v1/login/', CustomAuthToken.as_view()),
    path('api/v1/rest-auth/', include('rest_auth.urls')),
    # path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('accounts/', include('allauth.urls'))

]

# if settings.DEBUG:
# Serve static and media files from development server
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
