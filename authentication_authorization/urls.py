from django.urls import path, include
from .views import UserGroupsView, UserPermissionsView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('user-groups', UserGroupsView)
router.register('user-permissions', UserPermissionsView)

urlpatterns = [
    path('', include(router.urls))
]
