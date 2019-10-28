from django.urls import path, include
from .views import SocialAuthenticationView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('social-authentications', SocialAuthenticationView)

urlpatterns = [
    path('', include(router.urls))
]
