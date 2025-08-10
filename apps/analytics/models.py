from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class AnalyticsReport(models.Model):
    """Model for storing analytics reports"""
    REPORT_TYPES = [
        ('monthly_summary', 'Monthly Summary'),
        ('category_breakdown', 'Category Breakdown'),
        ('budget_analysis', 'Budget Analysis'),
        ('yearly_overview', 'Yearly Overview'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='analytics_reports')
    report_type = models.CharField(max_length=50, choices=REPORT_TYPES)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    data = models.JSONField(default=dict, blank=True)
    summary = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    report_file = models.FileField(upload_to='reports/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'report_type']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.title} - {self.user.email}"


class UserInsight(models.Model):
    """Model for storing user insights and recommendations"""
    INSIGHT_TYPES = [
        ('budget_warning', 'Budget Warning'),
        ('spending_pattern', 'Spending Pattern'),
        ('saving_opportunity', 'Saving Opportunity'),
        ('anomaly_detection', 'Anomaly Detection'),
        ('goal_achievement', 'Goal Achievement'),
    ]
    
    SEVERITY_CHOICES = [
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('critical', 'Critical'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='insights')
    insight_type = models.CharField(max_length=50, choices=INSIGHT_TYPES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='info')
    data = models.JSONField(default=dict, blank=True)
    recommendations = models.JSONField(default=list, blank=True)
    is_read = models.BooleanField(default=False)
    is_actionable = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'insight_type']),
            models.Index(fields=['severity']),
            models.Index(fields=['is_read']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.title} - {self.user.email}"


class CategoryAnalytics(models.Model):
    """Model for storing category-based analytics"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='category_analytics')
    category_name = models.CharField(max_length=100)
    month = models.DateField()
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transaction_count = models.IntegerField(default=0)
    average_transaction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    previous_month_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    month_over_month_change = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'category_name', 'month']
        ordering = ['-month', '-total_spent']
        indexes = [
            models.Index(fields=['user', 'category_name']),
            models.Index(fields=['month']),
            models.Index(fields=['total_spent']),
        ]

    def __str__(self):
        return f"{self.category_name} - {self.month.strftime('%Y-%m')} - {self.user.email}"
