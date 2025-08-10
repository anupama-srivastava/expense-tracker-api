from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, ExpenseViewSet, 
    RecurringExpenseViewSet, ExpenseSplitViewSet
)

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'expenses', ExpenseViewSet, basename='expense')
router.register(r'recurring', RecurringExpenseViewSet, basename='recurring-expense')
router.register(r'splits', ExpenseSplitViewSet, basename='expense-split')

urlpatterns = [
    path('', include(router.urls)),
]
