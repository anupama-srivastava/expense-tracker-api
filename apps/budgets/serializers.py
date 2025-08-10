from rest_framework import serializers
from .models import Budget


class BudgetSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = Budget
        fields = [
            'id', 'user', 'user_email', 'name', 'amount', 
            'period', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class BudgetCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ['name', 'amount', 'period']


class BudgetUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ['name', 'amount', 'period']
