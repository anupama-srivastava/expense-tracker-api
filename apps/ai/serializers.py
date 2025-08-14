from rest_framework import serializers
from .models import AIExpensePrediction, UserSpendingPattern, SmartBudgetRecommendation, AnomalyAlert


class AIExpensePredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIExpensePrediction
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class UserSpendingPatternSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSpendingPattern
        fields = '__all__'
        read_only_fields = ('id', 'created_at')


class SmartBudgetRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmartBudgetRecommendation
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class AnomalyAlertSerializer(serializers.ModelSerializer):
    expense_details = serializers.SerializerMethodField()

    class Meta:
        model = AnomalyAlert
        fields = ['id', 'expense', 'expense_details', 'anomaly_score', 
                 'expected_range', 'actual_amount', 'is_investigated', 
                 'created_at']

    def get_expense_details(self, obj):
        from apps.expenses.serializers import ExpenseSerializer
        return ExpenseSerializer(obj.expense).data


class AIChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=1000)
    context = serializers.JSONField(default=dict, required=False)


class AIChatResponseSerializer(serializers.Serializer):
    response = serializers.CharField()
    action = serializers.CharField(required=False)
    data = serializers.JSONField(required=False)
