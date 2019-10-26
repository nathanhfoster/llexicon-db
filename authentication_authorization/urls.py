from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('user-groups', views.UserGroupsView)
router.register('user-permissions', views.UserPermissionsView)

urlpatterns = [
    path('', include(router.urls))
]
