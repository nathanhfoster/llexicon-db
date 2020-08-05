from django.urls import path, include
from .views import SubscriptionView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('subscription', SubscriptionView)


urlpatterns = [
    path('', include(router.urls))
]
