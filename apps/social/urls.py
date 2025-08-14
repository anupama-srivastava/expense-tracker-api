from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SharedExpenseViewSet, FamilyBudgetViewSet, ExpenseChallengeViewSet

router = DefaultRouter()
router.register(r'shared-expenses', SharedExpenseViewSet)
router.register(r'family-budgets', FamilyBudgetViewSet)
router.register(r'expense-challenges', ExpenseChallengeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
