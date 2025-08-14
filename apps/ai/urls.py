from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AIExpensePredictionViewSet,
    UserSpendingPatternViewSet,
    SmartBudgetRecommendationViewSet,
    AnomalyAlertViewSet,
    AIChatViewSet
)

router = DefaultRouter()
router.register(r'predictions', AIExpensePredictionViewSet, basename='ai-predictions')
router.register(r'spending-patterns', UserSpendingPatternViewSet, basename='spending-patterns')
router.register(r'budget-recommendations', SmartBudgetRecommendationViewSet, basename='budget-recommendations')
router.register(r'anomaly-alerts', AnomalyAlertViewSet, basename='anomaly-alerts')
router.register(r'chat', AIChatViewSet, basename='ai-chat')

urlpatterns = [
    path('', include(router.urls)),
]
