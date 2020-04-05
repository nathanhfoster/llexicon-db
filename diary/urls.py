from django.urls import path, include
from .views import EntryView, TagView, PersonView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('tags', TagView)
router.register('people', PersonView)
router.register('entries', EntryView)


urlpatterns = [
    path('', include(router.urls))
]
