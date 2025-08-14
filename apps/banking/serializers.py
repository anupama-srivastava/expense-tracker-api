from rest_framework import serializers
from .models import BankAccount, Transaction, TransactionCategory, SyncLog


class BankAccountSerializer(serializers.ModelSerializer):
    """Serializer for BankAccount model"""
    
    class Meta:
        model = BankAccount
        fields = [
            'id', 'account_name', 'account_type', 'institution_name',
            'balance', 'currency', 'is_active', 'is_sync_enabled',
            'last_sync_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'last_sync_at']


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for Transaction model"""
    category_name = serializers.CharField(source='category', read_only=True)
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'transaction_id', 'amount', 'currency', 'description',
            'merchant_name', 'category', 'category_name', 'transaction_type',
            'transaction_date', 'posted_date', 'account_balance', 'is_pending',
            'is_manual', 'metadata', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class TransactionCategorySerializer(serializers.ModelSerializer):
    """Serializer for TransactionCategory model"""
    
    class Meta:
        model = TransactionCategory
        fields = ['id', 'name', 'parent_category', 'icon', 'color', 'is_active']
        read_only_fields = ['id']


class SyncLogSerializer(serializers.ModelSerializer):
    """Serializer for SyncLog model"""
    
    class Meta:
        model = SyncLog
        fields = [
            'id', 'status', 'transactions_added', 'transactions_updated',
            'error_message', 'started_at', 'completed_at', 'duration_seconds'
        ]
        read_only_fields = ['id', 'started_at', 'completed_at', 'duration_seconds']


class BankAccountCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating BankAccount with Plaid integration"""
    
    class Meta:
        model = BankAccount
        fields = [
            'account_name', 'account_type', 'institution_name',
            'balance', 'currency', 'is_active', 'is_sync_enabled'
        ]


class TransactionImportSerializer(serializers.Serializer):
    """Serializer for importing transactions"""
    account_id = serializers.IntegerField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    import_type = serializers.ChoiceField(choices=['manual', 'plaid', 'csv'])
    file = serializers.FileField(required=False, allow_null=True)


class TransactionFilterSerializer(serializers.Serializer):
    """Serializer for filtering transactions"""
    account_id = serializers.IntegerField(required=False)
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    category = serializers.CharField(required=False)
    transaction_type = serializers.CharField(required=False)
    min_amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    max_amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
