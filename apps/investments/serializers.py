from rest_framework import serializers
from .models import InvestmentAccount, Asset, Portfolio, CryptoHolding, CryptoTransaction, Performance, Goal


class InvestmentAccountSerializer(serializers.ModelSerializer):
    """Serializer for InvestmentAccount model"""
    
    class Meta:
        model = InvestmentAccount
        fields = [
            'id', 'account_name', 'account_type', 'institution_name',
            'total_value', 'currency', 'is_active', 'is_tax_advantaged',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AssetSerializer(serializers.ModelSerializer):
    """Serializer for Asset model"""
    
    class Meta:
        model = Asset
        fields = [
            'id', 'symbol', 'name', 'asset_type', 'sector', 'industry',
            'current_price', 'market_cap', 'currency', 'rank', 'last_updated'
        ]
        read_only_fields = ['id', 'last_updated']


class PortfolioSerializer(serializers.ModelSerializer):
    """Serializer for Portfolio model"""
    
    class Meta:
        model = Portfolio
        fields = [
            'id', 'investment_account', 'asset', 'quantity', 'average_cost',
            'current_value', 'unrealized_gain_loss', 'weight', 'last_price_update'
        ]
        read_only_fields = ['id', 'last_price_update']


class CryptoHoldingSerializer(serializers.ModelSerializer):
    """Serializer for CryptoHolding model"""
    
    class Meta:
        model = CryptoHolding
        fields = [
            'id', 'wallet', 'asset', 'quantity', 'average_cost',
            'current_value', 'unrealized_gain_loss', 'last_price_update'
        ]
        read_only_fields = ['id', 'last_price_update']


class CryptoTransactionSerializer(serializers.ModelSerializer):
    """Serializer for CryptoTransaction model"""
    
    class Meta:
        model = CryptoTransaction
        fields = [
            'id', 'wallet', 'asset', 'transaction_type', 'quantity',
            'price', 'amount', 'fees', 'transaction_date', 'tx_hash'
        ]
        read_only_fields = ['id', 'created_at']


class PerformanceSerializer(serializers.ModelSerializer):
    """Serializer for Performance model"""
    
    class Meta:
        model = Performance
        fields = [
            'id', 'investment_account', 'date', 'total_value', 'total_cost',
            'total_gain_loss', 'total_gain_loss_percent', 'daily_change'
        ]
        read_only_fields = ['id']


class GoalSerializer(serializers.ModelSerializer):
    """Serializer for Goal model"""
    
    class Meta:
        model = Goal
        fields = [
            'id', 'user', 'name', 'goal_typeNow let me create the serializers for the investments app:

<create_file>
<path>C:/Users/nupur/Desktop/expense-tracker-api/apps/investments/serializers.py</path>
<content>
from rest_framework import serializers
from .models import InvestmentAccount, Asset, Portfolio, Transaction, Performance, Goal


class InvestmentAccountSerializer(serializers.ModelSerializer):
    """Serializer for InvestmentAccount model"""
    
    class Meta:
        model = InvestmentAccount
        fields = [
            'id', 'account_name', 'account_type', 'institution_name',
            'account_number', 'total_value', 'currency', 'is_active',
            'is_tax_advantaged', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AssetSerializer(serializers.ModelSerializer):
    """Serializer for Asset model"""
    
    class Meta:
        model = Asset
        fields = [
            'id', 'symbol', 'name', 'asset_type', 'sector', 'industry',
            'exchange', 'currency', 'current_price', 'market_cap',
            'dividend_yield', 'pe_ratio', 'metadata', 'last_updated', 'created_at'
        ]
        read_only_fields = ['id', 'last_updated', 'created_at']


class PortfolioSerializer(serializers.ModelSerializer):
    """Serializer for Portfolio model"""
    
    class Meta:
        model = Portfolio
        fields = [
            'id', 'investment_account', 'asset', 'quantity',
            'average_cost', 'current_value', 'unrealized_gain_loss',
            'unrealized_gain_loss_percent', 'last_price_update', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for Transaction model"""
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'investment_account', 'asset', 'transaction_type',
            'quantity', 'price', 'amount', 'fees', 'currency',
            'transaction_date', 'settlement_date', 'description',
            'reference_id', 'metadata', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class PerformanceSerializer(serializers.ModelSerializer):
    """Serializer for Performance model"""
    
    class Meta:
        model = Performance
        fields = [
            'id', 'investment_account', 'date', 'total_value',
            'total_cost', 'total_gain_loss', 'total_gain_loss_percent',
            'daily_change', 'daily_change_percent', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class GoalSerializer(serializers.ModelSerializer):
    """Serializer for Goal model"""
    
    class Meta:
        model = Goal
        fields = [
            'id', 'user', 'name', 'goal_type', 'target_amount',
            'current_amount', 'target_date', 'priority', 'is_active',
            'description', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
