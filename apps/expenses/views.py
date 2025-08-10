from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Sum, Count, Avg
from django.utils import timezone
from datetime import datetime, timedelta

from .models import Category, Expense, RecurringExpense
from .serializers import (
    CategorySerializer, CategoryCreateSerializer,
    ExpenseSerializer, ExpenseCreateSerializer,
    RecurringExpenseSerializer, RecurringExpenseCreateSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing expense categories
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action == 'create':
            return CategoryCreateSerializer
        return CategorySerializer

    def get_queryset(self):
        """Filter categories for the current user"""
        return Category.objects.filter(is_active=True)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get category summary with expense counts"""
        categories = self.get_queryset()
        summary = []
        for category in categories:
            expense_count = Expense.objects.filter(
                category=category,
                user=request.user
            ).count()
            summary.append({
                'id': category.id,
                'name': category.name,
                'color': category.color,
                'expense_count': expense_count
            })
        return Response(summary)


class ExpenseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing expenses
    """
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['expense_type', 'category', 'date']
    search_fields = ['description']
    ordering_fields = ['date', 'amount', 'created_at']
    ordering = ['-date', '-created_at']

    def get_queryset(self):
        """Filter expenses for the current user"""
        return Expense.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return ExpenseCreateSerializer
        return ExpenseSerializer

    def perform_create(self, serializer):
        """Set the user to the current user"""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get expense summary"""
        expenses = self.get_queryset()
        summary = expenses.aggregate(
            total_expenses=Sum('amount', default=0),
            total_count=Count('id'),
            avg_amount=Avg('amount', default=0)
        )
        return Response(summary)

    @action(detail=False, methods=['get'])
    def monthly_summary(self, request):
        """Get monthly expense summary"""
        month = request.query_params.get('month')
        if month:
            expenses = self.get_queryset().filter(date__month=month)
        else:
            current_month = timezone.now().month
            expenses = self.get_queryset().filter(date__month=current_month)
        
        summary = expenses.aggregate(
            total=Sum('amount', default=0),
            count=Count('id'),
            avg=Avg('amount', default=0)
        )
        return Response(summary)

    @action(detail=False, methods=['get'])
    def category_breakdown(self, request):
        """Get expenses grouped by category"""
        expenses = self.get_queryset()
        breakdown = expenses.values('category__name').annotate(
            total=Sum('amount'),
            count=Count('id')
        ).order_by('-total')
        return Response(breakdown)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent expenses (last 30 days)"""
        thirty_days_ago = timezone.now() - timedelta(days=30)
        recent_expenses = self.get_queryset().filter(
            date__gte=thirty_days_ago
        ).order_by('-date')[:10]
        
        serializer = self.get_serializer(recent_expenses, many=True)
        return Response(serializer.data)


class RecurringExpenseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing recurring expenses
    """
    queryset = RecurringExpense.objects.all()
    serializer_class = RecurringExpenseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['frequency', 'is_active']
    search_fields = ['description']
    ordering_fields = ['next_occurrence', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter recurring expenses for the current user"""
        return RecurringExpense.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return RecurringExpenseCreateSerializer
        return RecurringExpenseSerializer

    def perform_create(self, serializer):
        """Set the user to the current user"""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get active recurring expenses"""
        active_expenses = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(active_expenses, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def generate_next_occurrence(self, request):
        """Generate next occurrence for recurring expenses"""
        recurring_expenses = self.get_queryset().filter(is_active=True)
        updated_count = 0
        
        for expense in recurring_expenses:
            if expense.next_occurrence <= timezone.now().date():
                # Create actual expense
                Expense.objects.create(
                    user=expense.user,
                    category=expense.category,
                    amount=expense.amount,
                    description=expense.description,
                    date=expense.next_occurrence,
                    is_recurring=True
                )
                
                # Update next occurrence
                expense.next_occurrence = expense.calculate_next_occurrence()
                expense.save()
                updated_count += 1
        
        return Response({
            'message': f'{updated_count} recurring expenses processed',
            'count': updated_count
        })
