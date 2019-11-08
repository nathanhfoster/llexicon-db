from django.urls import path, include
from .views import FileView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('files', FileView)


urlpatterns = [
    path('', include(router.urls))
]
