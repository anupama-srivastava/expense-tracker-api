from django.db import models
from django.contrib.auth import get_user_model
from djmoney.models.fields import MoneyField
from djmoney.money import Money
from django.core.validators import MinValueValidator

User = get_user_model()


class BankAccount(models.Model):
    """Model for storing bank account information"""
    ACCOUNT_TYPES = [
        ('checking', 'Checking'),
        ('savings', 'Savings'),
        ('credit_card', 'Credit Card'),
        ('investment', 'Investment'),
        ('loan', 'Loan'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bank_accounts')
    account_id = models.CharField(max_length=255, unique=True, help_text="External bank account ID")
    account_name = models.CharField(max_length=255)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    institution_name = models.CharField(max_length=255)
    balance = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    currency = models.CharField(max_length=3, default='USD')
    is_active = models.BooleanField(default=True)
    is_sync_enabled = models.BooleanField(default=True)
    last_sync_at = models.DateTimeField(null=True, blank=True)
    plaid_access_token = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'account_id']

    def __str__(self):
        return f"{self.institution_name} - {self.account_name}"


class Transaction(models.Model):
    """Model for storing bank transactions imported via Plaid or manual entry"""
    TRANSACTION_TYPES = [
        ('debit', 'Debit'),
        ('credit', 'Credit'),
    ]
    
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='transactions')
    transaction_id = models.CharField(max_length=255, unique=True, help_text="External transaction ID")
    amount = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    currency = models.CharField(max_length=3, default='USD')
    description = models.TextField()
    merchant_name = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    transaction_date = models.DateField()
    posted_date = models.DateField(null=True, blank=True)
    account_balance = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', null=True, blank=True)
    is_pending = models.BooleanField(default=False)
    is_manual = models.BooleanField(default=False, help_text="True if manually entered")
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-transaction_date', '-created_at']
        indexes = [
            models.Index(fields=['transaction_date']),
            models.Index(fields=['category']),
            models.Index(fields=['merchant_name']),
        ]

    def __str__(self):
        return f"{self.description} - {self.amount}"


class TransactionCategory(models.Model):
    """Model for categorizing transactions"""
    name = models.CharField(max_length=100, unique=True)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    icon = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=7, default='#007bff')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Transaction Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class SyncLog(models.Model):
    """Model for tracking bank account sync operations"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='sync_logs')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transactions_added = models.IntegerField(default=0)
    transactions_updated = models.IntegerField(default=0)
    error_message = models.TextField(blank=True, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return f"Sync {self.bank_account} - {self.status}"
