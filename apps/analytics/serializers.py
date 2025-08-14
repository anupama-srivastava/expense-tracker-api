from rest_framework import serializers
from .models import AnalyticsReport, UserInsight, CategoryAnalytics

class AnalyticsReportSerializer(serializers.ModelSerializer):
    """Serializer for Analytics Report model"""
    
    class Meta:
        model = AnalyticsReport
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'completed_at')

class AnalyticsReportCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating Analytics Reports"""
    
    class Meta:
        model = AnalyticsReport
        exclude = ('status', 'data', 'report_file', 'completed_at')
        
    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("End date must be after start date")
        return data

class UserInsightSerializer(serializers.ModelSerializer):
    """Serializer for User Insight model"""
    
    class Meta:
        model = UserInsight
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

class UserInsightCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating User Insights"""
    
    class Meta:
        model = UserInsight
        exclude = ('is_read',)

class CategoryAnalyticsSerializer(serializers.ModelSerializer):
    """Serializer for Category Analytics model"""
    
    class Meta:
        model = CategoryAnalytics
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

class CategoryAnalyticsCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating Category Analytics"""
    
    class Meta:
        model = CategoryAnalytics
        exclude = ('created_at', 'updated_at')

class DashboardDataSerializer(serializers.Serializer):
    """Serializer for dashboard data aggregation"""
    total_expenses = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_income = serializers.DecimalField(max_digits=12, decimal_places=2)
    net_savings = serializers.DecimalField(max_digits=12, decimal_places=2)
    monthly_average = serializers.DecimalField(max_digits=12, decimal_places=2)
    top_category = serializers.CharField()
    budget_utilization = serializers.FloatField()
    savings_rate = serializers.FloatField()
    expense_trend = serializers.ListField(child=serializers.DictField())
    category_breakdown = serializers.ListField(child=serializers.DictField())
    recent_transactions = serializers.ListField(child=serializers.DictField())

class ChartDataSerializer(serializers.Serializer):
    """Serializer for chart data"""
    labels = serializers.ListField(child=serializers.CharField())
    datasets = serializers.ListField(child=serializers.DictField())
    options = serializers.DictField(required=False)

class RealTimeUpdateSerializer(serializers.Serializer):
    """Serializer for real-time updates"""
    type = serializers.CharField()
    data = serializers.DictField()
    timestamp = serializers.DateTimeField()

class VoiceReportRequestSerializer(serializers.Serializer):
    """Serializer for voice report requests"""
    report_type = serializers.CharField()
    date_range = serializers.DictField(required=False)
    format = serializers.ChoiceField(choices=['summary', 'detailed', 'visual'])
    language = serializers.CharField(default='en')

class VoiceReportResponseSerializer(serializers.Serializer):
    """Serializer for voice report responses"""
    report_id = serializers.CharField()
    audio_url = serializers.URLField()
    transcript = serializers.CharField()
    summary = serializers.CharField()
    visual_data = serializers.DictField(required=False)

class ARVisualizationDataSerializer(serializers.Serializer):
    """Serializer for AR visualization data"""
    scene_id = serializers.CharField()
    objects = serializers.ListField(child=serializers.DictField())
    interactions = serializers.ListField(child=serializers.DictField())
    metadata = serializers.DictField()

class SmartNotificationSerializer(serializers.Serializer):
    """Serializer for smart notifications"""
    notification_type = serializers.CharField()
    title = serializers.CharField()
    message = serializers.CharField()
    priority = serializers.ChoiceField(choices=['low', 'medium', 'high', 'critical'])
    actions = serializers.ListField(child=serializers.DictField(), required=False)
    context = serializers.DictField(required=False)
