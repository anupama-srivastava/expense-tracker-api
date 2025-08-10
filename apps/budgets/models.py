from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Budget(models.Model):
    """Model for storing budgets"""
    BUDGET_TYPES = [
        ('monthly', 'Monthly'),
        ('weekly', 'Weekly'),
        ('yearly', 'Yearly'),
        ('custom', 'Custom'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    budget_type = models.CharField(max_length=20, choices=BUDGET_TYPES, default='monthly')
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    alert_threshold = models.DecimalField(max_digits=5, decimal_places=2, default=80.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['start_date', 'end_date']),
        ]

    def __str__(self):
        return f"{self.name} - ${self.amount} - {self.user.email}"

    @property
    def remaining(self):
        return self.amount - self.spent

    @property
    def percentage_used(self):
        if self.amount > 0:
            return (self.spent / self.amount) * 100
        return 0


class BudgetCategory(models.Model):
    """Model for linking budgets to categories"""
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='categories')
    category_name = models.CharField(max_length=100)
    allocated_amount = models.DecimalField(max_digits=10, decimal_places=2)
    spent_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['budget', 'category_name']
        ordering = ['category_name']

    def __str__(self):
        return f"{self.budget.name} - {self.category_name}"

    @property
    def remaining(self):
        return self.allocated_amount - self.spent_amount

    @property
    def percentage_used(self):
        if self.allocated_amount > 0:
            return (self.spent_amount / self.allocated_amount) * 100
        return 0


class BudgetAlert(models.Model):
    """Model for storing budget alerts"""
    ALERT_TYPES = [
        ('threshold_reached', 'Threshold Reached'),
        ('budget_exceeded', 'Budget Exceeded'),
        ('goal_achieved', 'Goal Achieved'),
    ]
    
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='alerts')
    alert_type = models.CharField(max_length=50, choices=ALERT_TYPES)
    message = models.TextField()
    threshold_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['budget', 'is_read']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.budget.name} - {self.alert_type}"
