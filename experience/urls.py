from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()

router.register('experiences', views.ExperienceView)
router.register('experience/bulletpoints', views.BulletPointsView)
router.register('experience/media', views.MediaView)

urlpatterns = [
    path('', include(router.urls))
]
