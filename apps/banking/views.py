from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count, Avg
from django.utils import timezone
from datetime import datetime, timedelta

from .models import BankAccount, Transaction, TransactionCategory, SyncLog
from .serializers import (
    BankAccountSerializer, TransactionSerializer, TransactionCategorySerializer,
    SyncLogSerializer, BankAccountCreateSerializer, TransactionImportSerializer,
    TransactionFilterSerializer
)


class BankAccountViewSet(viewsets.ModelViewSet):
    """ViewSet for managing bank accounts"""
    serializer_class = BankAccountSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['account_type', 'is_active', 'is_sync_enabled']

    def get_queryset(self):
        return BankAccount.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def sync_transactions(self, request, pk=None):
        """Sync transactions for a specific bank account"""
        account = self.get_object()
        
        # Create sync log
        sync_log = SyncLog.objects.create(
            bank_account=account,
            status='in_progress'
        )
        
        try:
            # Here you would integrate with Plaid API
            # For now, we'll simulate the sync
            transactions_added = 0
            transactions_updated = 0
            
            # Update sync log
            sync_log.status = 'completed'
            sync_log.transactions_added = transactions_added
            sync_log.transactions_updated = transactions_updated
            sync_log.completed_at = timezone.now()
            sync_log.duration_seconds = 30  # Simulated duration
            sync_log.save()
            
            account.last_sync_at = timezone.now()
            account.save()
            
            return Response({
                'message': 'Sync completed successfully',
                'transactions_added': transactions_added,
                'transactions_updated': transactions_updated
            })
            
        except Exception as e:
            sync_log.status = 'failed'
            sync_log.error_message = str(e)
            sync_log.completed_at = timezone.now()
            sync_log.save()
            
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get summary of all bank accounts"""
        accounts = self.get_queryset()
        total_balance = accounts.aggregate(total=Sum('balance'))['total'] or 0
        
        account_summary = accounts.values('account_type').annotate(
            count=Count('id'),
            total_balance=Sum('balance')
        )
        
        return Response({
            'total_accounts': accounts.count(),
            'total_balance': total_balance,
            'account_summary': account_summary
        })


class TransactionViewSet(viewsets.ModelViewSet):
    """ViewSet for managing transactions"""
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['transaction_type', 'category', 'is_pending']

    def get_queryset(self):
        return Transaction.objects.filter(
            bank_account__user=self.request.user
        ).select_related('bank_account')

    @action(detail=False, methods=['post'])
    def import_transactions(self, request):
        """Import transactions from various sources"""
        serializer = TransactionImportSerializer(data=request.data)
        if serializer.is_valid():
            # Here you would implement actual import logic
            # For now, we'll return a success response
            return Response({
                'message': 'Import started',
                'import_type': serializer.validated_data['import_type']
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def analytics(self, request):
        """Get transaction analytics"""
        queryset = self.get_queryset()
        
        # Date range filtering
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(transaction_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(transaction_date__lte=end_date)
        
        # Calculate analytics
        total_spent = queryset.filter(transaction_type='debit').aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        total_received = queryset.filter(transaction_type='credit').aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        category_spending = queryset.filter(transaction_type='debit').values(
            'category'
        ).annotate(
            total=Sum('amount'),
            count=Count('id')
        ).order_by('-total')
        
        daily_spending = queryset.filter(transaction_type='debit').values(
            'transaction_date'
        ).annotate(
            total=Sum('amount'),
            count=Count('id')
        ).order_by('transaction_date')
        
        return Response({
            'total_spent': total_spent,
            'total_received': total_received,
            'net_amount': total_received - total_spent,
            'category_spending': category_spending,
            'daily_spending': daily_spending
        })


class TransactionCategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for managing transaction categories"""
    serializer_class = TransactionCategorySerializer
    permission_classes = [IsAuthenticated]
    queryset = TransactionCategory.objects.filter(is_active=True)

    def get_queryset(self):
        return TransactionCategory.objects.filter(is_active=True)


class SyncLogViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing sync logs"""
    serializer_class = SyncLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SyncLog.objects.filter(
            bank_account__user=self.request.user
        ).select_related('bank_account')
