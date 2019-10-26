from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()

router.register('educations', views.EducationView)
router.register('education/media', views.MediaView)

urlpatterns = [
    path('', include(router.urls))
]
