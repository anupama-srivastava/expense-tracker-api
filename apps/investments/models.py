from django.db import models
from django.contrib.auth import get_user_model
from djmoney.models.fields import MoneyField
from djmoney.money import Money
from django.core.validators import MinValueValidator

User = get_user_model()


class InvestmentAccount(models.Model):
    """Model for storing investment account information"""
    ACCOUNT_TYPES = [
        ('brokerage', 'Brokerage'),
        ('401k', '401(k)'),
        ('ira', 'IRA'),
        ('roth_ira', 'Roth IRA'),
        ('529', '529 Plan'),
        ('hsa', 'HSA'),
        ('mutual_fund', 'Mutual Fund'),
        ('etf', 'ETF'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='investment_accounts')
    account_name = models.CharField(max_length=255)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    institution_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=100, blank=True, null=True)
    total_value = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    currency = models.CharField(max_length=3, default='USD')
    is_active = models.BooleanField(default=True)
    is_tax_advantaged = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.account_name} - {self.institution_name}"


class Asset(models.Model):
    """Model for storing asset information (stocks, bonds, ETFs, etc.)"""
    ASSET_TYPES = [
        ('stock', 'Stock'),
        ('bond', 'Bond'),
        ('etf', 'ETF'),
        ('mutual_fund', 'Mutual Fund'),
        ('crypto', 'Cryptocurrency'),
        ('commodity', 'Commodity'),
        ('reit', 'REIT'),
        ('option', 'Option'),
        ('future', 'Future'),
    ]
    
    symbol = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPES)
    sector = models.CharField(max_length=100, blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True, null=True)
    exchange = models.CharField(max_length=50, blank=True, null=True)
    currency = models.CharField(max_length=3, default='USD')
    current_price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', null=True, blank=True)
    market_cap = MoneyField(max_digits=20, decimal_places=2, default_currency='USD', null=True, blank=True)
    dividend_yield = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    pe_ratio = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['symbol']

    def __str__(self):
        return f"{self.symbol} - {self.name}"


class Portfolio(models.Model):
    """Model for storing portfolio holdings"""
    investment_account = models.ForeignKey(InvestmentAccount, on_delete=models.CASCADE, related_name='portfolios')
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='portfolios')
    quantity = models.DecimalField(max_digits=20, decimal_places=8, validators=[MinValueValidator(0)])
    average_cost = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    current_value = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', null=True, blank=True)
    unrealized_gain_loss = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', null=True, blank=True)
    unrealized_gain_loss_percent = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    last_price_update = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['investment_account', 'asset']
        ordering = ['-current_value']

    def __str__(self):
        return f"{self.investment_account} - {self.asset.symbol}"


class Transaction(models.Model):
    """Model for storing investment transactions (buy, sell, dividends, etc.)"""
    TRANSACTION_TYPES = [
        ('buy', 'Buy'),
        ('sell', 'Sell'),
        ('dividend', 'Dividend'),
        ('interest', 'Interest'),
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('fee', 'Fee'),
        ('split', 'Stock Split'),
        ('merger', 'Merger'),
    ]
    
    investment_account = models.ForeignKey(InvestmentAccount, on_delete=models.CASCADE, related_name='transactions')
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    quantity = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    amount = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    fees = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', default=0)
    currency = models.CharField(max_length=3, default='USD')
    transaction_date = models.DateField()
    settlement_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    reference_id = models.CharField(max_length=255, blank=True, null=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-transaction_date', '-created_at']
        indexes = [
            models.Index(fields=['transaction_date']),
            models.Index(fields=['transaction_type']),
            models.Index(fields=['asset']),
        ]

    def __str__(self):
        return f"{self.transaction_type} - {self.asset.symbol} - {self.amount}"


class Performance(models.Model):
    """Model for storing portfolio performance metrics"""
    investment_account = models.ForeignKey(InvestmentAccount, on_delete=models.CASCADE, related_name='performance_metrics')
    date = models.DateField()
    total_value = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    total_cost = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    total_gain_loss = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    total_gain_loss_percent = models.DecimalField(max_digits=8, decimal_places=2)
    daily_change = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    daily_change_percent = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['investment_account', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.investment_account} - {self.date} - {self.total_value}"


class Goal(models.Model):
    """Model for storing investment goals"""
    GOAL_TYPES = [
        ('retirement', 'Retirement'),
        ('emergency_fund', 'Emergency Fund'),
        ('house', 'House Purchase'),
        ('education', 'Education'),
        ('vacation', 'Vacation'),
        ('wedding', 'Wedding'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='investment_goals')
    name = models.CharField(max_length=255)
    goal_type = models.CharField(max_length=20, choices=GOAL_TYPES)
    target_amount = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    current_amount = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', default=0)
    target_date = models.DateField()
    priority = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['priority', '-created_at']

    def __str__(self):
        return f"{self.name} - {self.target_amount}"

    @property
    def progress_percent(self):
        if self.target_amount > 0:
            return (self.current_amount / self.target_amount) * 100
        return 0
