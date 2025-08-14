from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField

User = get_user_model()


class AIExpensePrediction(models.Model):
    """Model for AI-powered expense predictions"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_predictions')
    predicted_amount = models.DecimalField(max_digits=10, decimal_places=2)
    actual_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    category = models.CharField(max_length=100)
    subcategory = models.CharField(max_length=100, blank=True)
    prediction_date = models.DateField()
    confidence_score = models.FloatField()
    prediction_type = models.CharField(max_length=20, choices=[
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly')
    ], default='monthly')
    features_used = JSONField(default=dict)
    model_version = models.CharField(max_length=20, default='v1.0')
    is_accurate = models.BooleanField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'prediction_date']),
            models.Index(fields=['category', 'prediction_type']),
            models.Index(fields=['model_version']),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.category} - {self.predicted_amount}"


class UserSpendingPattern(models.Model):
    """Model for storing user spending patterns for ML training"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='spending_patterns')
    category = models.CharField(max_length=100)
    subcategory = models.CharField(max_length=100, blank=True)
    day_of_week = models.IntegerField()  # 0-6 (Monday-Sunday)
    time_of_day = models.IntegerField()  # 0-23
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=200, blank=True)
    payment_method = models.CharField(max_length=20, blank=True)
    weather_data = JSONField(default=dict, blank=True)
    transaction_type = models.CharField(max_length=20, choices=[
        ('expense', 'Expense'),
        ('income', 'Income')
    ], default='expense')
    merchant = models.CharField(max_length=200, blank=True)
    tags = JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'category', 'subcategory']),
            models.Index(fields=['day_of_week', 'time_of_day']),
            models.Index(fields=['transaction_type']),
        ]


class SmartBudgetRecommendation(models.Model):
    """Model for AI-generated budget recommendations"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budget_recommendations')
    category = models.CharField(max_length=100)
    subcategory = models.CharField(max_length=100, blank=True)
    recommended_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_spending = models.DecimalField(max_digits=10, decimal_places=2)
    previous_spending = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    reasoning = models.TextField()
    confidence_level = models.FloatField()
    risk_level = models.CharField(max_length=10, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ], default='medium')
    is_accepted = models.BooleanField(default=False)
    accepted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'category']),
            models.Index(fields=['risk_level', 'confidence_level']),
        ]


class AnomalyAlert(models.Model):
    """Model for storing unusual spending alerts"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='anomaly_alerts')
    expense = models.ForeignKey('expenses.Expense', on_delete=models.CASCADE, related_name='anomaly_alerts')
    anomaly_score = models.FloatField()
    anomaly_type = models.CharField(max_length=20, choices=[
        ('amount', 'Unusual Amount'),
        ('frequency', 'Unusual Frequency'),
        ('timing', 'Unusual Timing'),
        ('location', 'Unusual Location'),
        ('category', 'Unusual Category')
    ], default='amount')
    expected_range = JSONField(default=dict)
    actual_amount = models.DecimalField(max_digits=10, decimal_places=2)
    severity = models.CharField(max_length=10, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical')
    ], default='medium')
    is_investigated = models.BooleanField(default=False)
    investigation_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'severity']),
            models.Index(fields=['anomaly_type']),
        ]


class MLModelVersion(models.Model):
    """Model for tracking ML model versions and performance"""
    model_name = models.CharField(max_length=50)
    version = models.CharField(max_length=20)
    accuracy = models.FloatField()
    precision = models.FloatField()
    recall = models.FloatField()
    f1_score = models.FloatField()
    training_data_size = models.IntegerField()
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['model_name', 'version']
        indexes = [
            models.Index(fields=['model_name', 'is_active']),
        ]

    def __str__(self):
        return f"{self.model_name} - {self.version}"


class SmartCategoryPrediction(models.Model):
    """Model for AI-powered expense categorization"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='category_predictions')
    expense = models.ForeignKey('expenses.Expense', on_delete=models.CASCADE, related_name='category_predictions')
    predicted_category = models.CharField(max_length=100)
    confidence_score = models.FloatField()
    alternative_categories = JSONField(default=list)
    is_correct = models.BooleanField(null=True, blank=True)
    feedback_provided = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'predicted_category']),
            models.Index(fields=['confidence_score']),
        ]
