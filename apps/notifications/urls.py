from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet, NotificationPreferenceViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'preferences', NotificationPreferenceViewSet, basename='notification-preference')

urlpatterns = [
    path('', include(router.urls)),
]
