from django.urls import path, include
from .views import VersionView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('versions', VersionView)


urlpatterns = [
    path('', include(router.urls))
]
