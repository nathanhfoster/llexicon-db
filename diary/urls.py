from django.urls import path, include
from .views import TagView, EntryView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('tags', TagView)
router.register('entries', EntryView)


urlpatterns = [
    path('', include(router.urls))
]
