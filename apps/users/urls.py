from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserProfileViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'profiles', UserProfileViewSet, basename='user-profile')

urlpatterns = [
    path('', include(router.urls)),
]
