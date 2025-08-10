from rest_framework import serializers
from .models import Category, Expense, RecurringExpense, ExpenseSplit


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'color', 'icon', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ExpenseSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Expense
        fields = [
            'id', 'user', 'user_email', 'category', 'category_name', 'title',
            'description', 'amount', 'expense_type', 'payment_method',
            'transaction_date', 'location', 'receipt', 'tags', 'is_recurring',
            'recurring_frequency', 'is_split', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ExpenseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = [
            'category', 'title', 'description', 'amount', 'expense_type',
            'payment_method', 'transaction_date', 'location', 'receipt',
            'tags', 'is_recurring', 'recurring_frequency', 'is_split'
        ]


class RecurringExpenseSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = RecurringExpense
        fields = [
            'id', 'user', 'user_email', 'category', 'category_name', 'title',
            'description', 'amount', 'frequency', 'start_date', 'end_date',
            'next_occurrence', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class RecurringExpenseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurringExpense
        fields = [
            'category', 'title', 'description', 'amount', 'frequency',
            'start_date', 'end_date', 'is_active'
        ]


class ExpenseSplitSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = ExpenseSplit
        fields = [
            'id', 'expense', 'user', 'user_email',
            'amount', 'is_paid', 'paid_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ExpenseSplitCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseSplit
        fields = ['expense', 'user', 'amount']
