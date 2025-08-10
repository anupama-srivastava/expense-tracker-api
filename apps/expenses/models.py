from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    """Model for expense categories"""
    name = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=7, default='#007bff')
    icon = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Expense(models.Model):
    """Model for storing expenses"""
    EXPENSE_TYPES = [
        ('expense', 'Expense'),
        ('income', 'Income'),
    ]
    
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('upi', 'UPI'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='expenses')
    expense_type = models.CharField(max_length=10, choices=EXPENSE_TYPES, default='expense')
    title = models.CharField(max_length=200)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cash')
    transaction_date = models.DateField()
    location = models.CharField(max_length=200, blank=True)
    receipt = models.ImageField(upload_to='receipts/', blank=True, null=True)
    tags = models.JSONField(default=list, blank=True)
    is_recurring = models.BooleanField(default=False)
    recurring_frequency = models.CharField(max_length=20, blank=True)
    is_split = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-transaction_date', '-created_at']
        indexes = [
            models.Index(fields=['user', 'transaction_date']),
            models.Index(fields=['category']),
            models.Index(fields=['expense_type']),
        ]

    def __str__(self):
        return f"{self.title} - ${self.amount} - {self.user.email}"


class RecurringExpense(models.Model):
    """Model for storing recurring expenses"""
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recurring_expenses')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='recurring_expenses')
    title = models.CharField(max_length=200)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    next_occurrence = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['next_occurrence']),
        ]

    def __str__(self):
        return f"{self.title} - {self.frequency} - {self.user.email}"


class ExpenseSplit(models.Model):
    """Model for storing expense splits between users"""
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='splits')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expense_splits')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['expense', 'user']
        indexes = [
            models.Index(fields=['user', 'is_paid']),
            models.Index(fields=['expense']),
        ]

    def __str__(self):
        return f"{self.expense.title} - {self.user.email} - ${self.amount}"
