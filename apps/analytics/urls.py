from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnalyticsReportViewSet, UserInsightViewSet, CategoryAnalyticsViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'reports', AnalyticsReportViewSet, basename='analytics-report')
router.register(r'insights', UserInsightViewSet, basename='user-insight')
router.register(r'categories', CategoryAnalyticsViewSet, basename='category-analytics')

urlpatterns = [
    path('', include(router.urls)),
]
