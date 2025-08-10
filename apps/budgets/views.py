from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model

from .models import Budget
from .serializers import BudgetSerializer, BudgetCreateSerializer, BudgetUpdateSerializer

User = get_user_model()


class BudgetViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing budgets
    """
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['period', 'created_at']
    search_fields = ['name']
    ordering_fields = ['created_at', 'amount']
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter budgets for the current user"""
        return Budget.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return BudgetCreateSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return BudgetUpdateSerializer
        return BudgetSerializer

    def perform_create(self, serializer):
        """Set the user to the current user"""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get budget summary for current user"""
        queryset = self.get_queryset()
        
        # Date range filter
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)
        
        summary = queryset.aggregate(
            total_budgets=Count('id'),
            total_amount=Sum('amount')
        )
        
        return Response(summary)

    @action(detail=False, methods=['get'])
    def by_period(self, request):
        """Get budgets grouped by period"""
        queryset = self.get_queryset()
        
        period_data = queryset.values('period').annotate(
            total_amount=Sum('amount'),
            count=Count('id')
        ).order_by('-total_amount')
        
        return Response(period_data)

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get active budgets"""
        active_budgets = self.get_queryset()
        serializer = self.get_serializer(active_budgets, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent budgets (last 30 days)"""
        thirty_days_ago = timezone.now() - timedelta(days=30)
        recent_budgets = self.get_queryset().filter(
            created_at__gte=thirty_days_ago
        ).order_by('-created_at')[:10]
        
        serializer = self.get_serializer(recent_budgets, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def summary_by_period(self, request):
        """Get budget summary grouped by period"""
        queryset = self.get_queryset()
        
        summary = queryset.values('period').annotate(
            total_amount=Sum('amount'),
            count=Count('id')
        ).order_by('-total_amount')
        
        return Response(summary)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent budgets (last 30 days)"""
        thirty_days_ago = timezone.now() - timedelta(days=30)
        recent_budgets = self.get_queryset().filter(
            created_at__gte=thirty_days_ago
        ).order_by('-created_at')[:10]
        
        serializer = self.get_serializer(recent_budgets, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def summary_by_period(self, request):
        """Get budget summary grouped by period"""
        queryset = self.get_queryset()
        
        summary = queryset.values('period').annotate(
            total_amount=Sum('amount'),
            count=Count('id')
        ).order_by('-total_amount')
        
        return Response(summary)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent budgets (last 30 days)"""
        thirty_days_ago = timezone.now() - timedelta(days=30)
        recent_budgets = self.get_queryset().filter(
            created_at__gte=thirty_days_ago
        ).order_by('-created_at')[:10]
        
        serializer = self.get_serializer(recent_budgets, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def summary_by_period(self, request):
        """Get budget summary grouped by period"""
        queryset = self.get_queryset()
        
        summary = queryset.values('period').annotate(
            total_amount=Sum('amount'),
            count=Count('id')
        ).order_by('-total_amount')
        
        return Response(summary)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent budgets (last 30 days)"""
        thirty_days_ago = timezone.now() - timedelta(days=30)
        recent_budgets = self.get_queryset().filter(
            created_at__gte=thirty_days_ago
        ).order_by('-created_at')[:10]
        
        serializer = self.get_serializer(recent_budgets, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def summary_by_period(self, request):
        """Get budget summary grouped by period"""
        queryset = self.get_queryset()
        
        summary = queryset.values('period').annotate(
            total_amount=Sum('amount'),
            count=Count('id')
        ).order_by('-total_amount')
        
        return Response(summary)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent budgets (last 30 days)"""
        thirty_days_ago = timezone.now() - timedelta(days=30)
        recent_budgets = self.get_queryset().filter(
            created_at__gte=thirty_days_ago
        ).order_by('-created_at')[:10]
        
        serializer = self.get_serializer(recent_budgets, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def summary_by_period(self, request):
        """Get budget summary grouped by period"""
        queryset = self.get_queryset()
        
        summary = queryset.values('period').annotate(
            total_amount=Sum('amount'),
            count=Count('id')
        ).order_by('-total_amount')
        
        return Response(summary)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent budgets (last 30 days)"""
        thirty_days_ago = timezone.now() - timedelta(days=30)
        recent_budgets = self.get_queryset().filter(
            created_at__gte=thirty_days_ago
        ).order_by('-created_at')[:10]
        
        serializer = self.get_serializer(recent_budgets, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def summary_by_period(self, request):
        """Get budget summary grouped by period"""
        queryset = self.get_queryset()
        
        summary = queryset.values('period').annotate(
            total_amount=Sum('amount'),
            count=Count('id')
        ).order_by('-total_amount')
        
        return Response(summary)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent budgets (last 30 days)
