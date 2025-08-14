from django.db import models
from django.contrib.auth import get_user_model
from djmoney.models.fields import MoneyField
from djmoney.money import Money
from django.core.validators import MinValueValidator

User = get_user_model()


class Exchange(models.Model):
    """Model for storing cryptocurrency exchange information"""
    name = models.CharField(max_length=100, unique=True)
    api_key = models.CharField(max_length=255, blank=True, null=True)
    api_secret = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    website = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class CryptoAsset(models.Model):
    """Model for storing cryptocurrency asset information"""
    symbol = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=100, unique=True)
    image_url = models.URLField(blank=True, null=True)
    current_price = MoneyField(max_digits=20, decimal_places=8, default_currency='USD')
    market_cap = MoneyField(max_digits=20, decimal_places=2, default_currency='USD', null=True, blank=True)
    volume_24h = MoneyField(max_digits=20, decimal_places=2, default_currency='USD', null=True, blank=True)
    price_change_24h = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    price_change_percentage_24h = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    circulating_supply = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    total_supply = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    max_supply = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    rank = models.IntegerField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['rank', 'symbol']

    def __str__(self):
        return f"{self.symbol} - {self.name}"


class Wallet(models.Model):
    """Model for storing cryptocurrency wallet information"""
    WALLET_TYPES = [
        ('exchange', 'Exchange Wallet'),
        ('software', 'Software Wallet'),
        ('hardware', 'Hardware Wallet'),
        ('paper', 'Paper Wallet'),
        ('custodial', 'Custodial Wallet'),
        ('non_custodial', 'Non-Custodial Wallet'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='crypto_wallets')
    name = models.CharField(max_length=255)
    wallet_type = models.CharField(max_length=20, choices=WALLET_TYPES)
    address = models.CharField(max_length=255, blank=True, null=True)
    exchange = models.ForeignKey(Exchange, on_delete=models.SET_NULL, null=True, blank=True)
    currency = models.CharField(max_length=3, default='USD')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.wallet_type}"


class CryptoHolding(models.Model):
    """Model for storing cryptocurrency holdings"""
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='holdings')
    asset = models.ForeignKey(CryptoAsset, on_delete=models.CASCADE, related_name='holdings')
    quantity = models.DecimalField(max_digits=20, decimal_places=8, validators=[MinValueValidator(0)])
    average_cost = MoneyField(max_digits=20, decimal_places=8, default_currency='USD')
    current_value = MoneyField(max_digits=20, decimal_places=2, default_currency='USD', null=True, blank=True)
    unrealized_gain_loss = MoneyField(max_digits=20, decimal_places=2, default_currency='USD', null=True, blank=True)
    unrealized_gain_loss_percent = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    last_price_update = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['wallet', 'asset']
        ordering = ['-current_value']

    def __str__(self):
        return f"{self.wallet} - {self.asset.symbol}"


class CryptoTransaction(models.Model):
    """Model for storing cryptocurrency transactions"""
    TRANSACTION_TYPES = [
        ('buy', 'Buy'),
        ('sell', 'Sell'),
        ('transfer', 'Transfer'),
        ('receive', 'Receive'),
        ('send', 'Send'),
        ('trade', 'Trade'),
        ('staking_reward', 'Staking Reward'),
        ('mining_reward', 'Mining Reward'),
        ('airdrop', 'Airdrop'),
        ('fee', 'Fee'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='crypto_transactions')
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    asset = models.ForeignKey(CryptoAsset, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    quantity = models.DecimalField(max_digits=20, decimal_places=8)
    price = MoneyField(max_digits=20, decimal_places=8, default_currency='USD')
    amount = MoneyField(max_digits=20, decimal_places=2, default_currency='USD')
    fees = MoneyField(max_digits=20, decimal_places=2, default_currency='USD', default=0)
    currency = models.CharField(max_length=3, default='USD')
    transaction_date = models.DateTimeField()
    tx_hash = models.CharField(max_length=255, blank=True, null=True)
    from_address = models.CharField(max_length=255, blank=True, null=True)
    to_address = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-transaction_date', '-created_at']
        indexes = [
            models.Index(fields=['transaction_date']),
            models.Index(fields=['transaction_type']),
            models.Index(fields=['tx_hash']),
        ]

    def __str__(self):
        return f"{self.transaction_type} - {self.asset.symbol} - {self.amount}"


class StakingReward(models.Model):
    """Model for storing staking rewards"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='staking_rewards')
    asset = models.ForeignKey(CryptoAsset, on_delete=models.CASCADE, related_name='staking_rewards')
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='staking_rewards')
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    reward_date = models.DateField()
    usd_value = MoneyField(max_digits=20, decimal_places=2, default_currency='USD')
    currency = models.CharField(max_length=3, default='USD')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-reward_date', '-created_at']

    def __str__(self):
        return f"{self.asset.symbol} Staking Reward - {self.amount}"


class PriceHistory(models.Model):
    """Model for storing cryptocurrency price history"""
    asset = models.ForeignKey(CryptoAsset, on_delete=models.CASCADE, related_name='price_history')
    price = MoneyField(max_digits=20, decimal_places=8, default_currency='USD')
    market_cap = MoneyField(max_digits=20, decimal_places=2, default_currency='USD', null=True, blank=True)
    volume_24h = MoneyField(max_digits=20, decimal_places=2, default_currency='USD', null=True, blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['asset', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.asset.symbol} - {self.date} - {self.price}"
