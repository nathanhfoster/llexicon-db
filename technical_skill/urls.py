from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()

router.register('specializations', views.SpecializationView)
router.register('skills', views.SkillView)
router.register('specialization/skill/experience',
                views.SpecializationSkillExperienceView)

urlpatterns = [
    path('', include(router.urls))
]
