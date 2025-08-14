from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField

User = get_user_model()


class SharedExpense(models.Model):
    """Model for shared expenses between multiple users"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_shared_expenses')
    participants = models.ManyToManyField(User, through='SharedExpenseParticipant', related_name='shared_expenses')
    category = models.ForeignKey('expenses.Category', on_delete=models.CASCADE, related_name='shared_expenses')
    transaction_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_by', 'transaction_date']),
            models.Index(fields=['transaction_date']),
        ]


class SharedExpenseParticipant(models.Model):
    """Model for participants in shared expenses"""
    shared_expense = models.ForeignKey(SharedExpense, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_expense_participations')
    amount_owed = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_paid']),
            models.Index(fields=['shared_expense', 'user']),
        ]


class FamilyBudget(models.Model):
    """Model for family budgets with multiple users"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    total_budget = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_family_budgets')
    members = models.ManyToManyField(User, through='FamilyBudgetMember', related_name='family_budgets')
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_by', 'start_date']),
            models.Index(fields=['start_date']),
        ]


class FamilyBudgetMember(models.Model):
    """Model for members in family budgets"""
    family_budget = models.ForeignKey(FamilyBudget, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='family_budget_memberships')
    allocated_amount = models.DecimalField(max_digits=10, decimal_places=2)
    spent_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_admin']),
            models.Index(fields=['family_budget', 'user']),
        ]


class ExpenseChallenge(models.Model):
    """Model for expense challenges and gamification"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_challenges')
    participants = models.ManyToManyField(User, through='ExpenseChallengeParticipant', related_name='expense_challenges')
    goal_type = models.CharField(max_length=50, choices=[
        ('savings', 'Savings Challenge'),
        ('spending', 'Spending Challenge'),
        ('budget', 'Budget Challenge'),
        ('category', 'Category Challenge'),
    ])
    goal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    goal_category = models.ForeignKey('expenses.Category', on_delete=models.CASCADE, related_name='challenges', blank=True, null=True)
    rules = JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_by', 'start_date']),
            models.Index(fields=['start_date']),
        ]


class ExpenseChallengeParticipant(models.Model):
    """Model for participants in expense challenges"""
    expense_challenge = models.ForeignKey(ExpenseChallenge, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expense_challenge_participations')
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)
    rank = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_completed']),
            models.Index(fields=['expense_challenge', 'user']),
        ]


class SocialFeed(models.Model):
    """Model for social feed and activity sharing"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='social_feeds')
    content = models.TextField()
    image = models.ImageField(upload_to='social_feed/', blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='liked_feeds', blank=True)
    comments = models.ManyToManyField(User, through='SocialFeedComment', related_name='commented_feeds', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['created_at']),
        ]


class SocialFeedComment(models.Model):
    """Model for comments on social feed"""
    social_feed = models.ForeignKey(SocialFeed, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='social_feed_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['social_feed', 'created_at']),
            models.Index(fields=['user', 'created_at']),
        ]


class Notification(models.Model):
    """Model for social notifications"""
    NOTIFICATION_TYPES = [
        ('shared_expense_created', 'Shared Expense Created'),
        ('shared_expense_updated', 'Shared Expense Updated'),
        ('challenge_invitation', 'Challenge Invitation'),
        ('challenge_completed', 'Challenge Completed'),
        ('friend_request', 'Friend Request'),
        ('expense_like', 'Expense Liked'),
        ('comment_added', 'Comment Added'),
        ('goal_achieved', 'Goal Achieved'),
        ('milestone_reached', 'Milestone Reached'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='social_notifications')
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    related_object = models.ForeignKey('expenses.Expense', on_delete=models.CASCADE, related_name='social_notifications', blank=True, null=True)
    is_readNow let me create the models for the social features:

<create_file>
<path>C:/Users/nupur/Desktop/expense-tracker-api/apps/social/models.py</path>
<content>
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class SharedExpense(models.Model):
    """Model for shared expenses among users"""
    users = models.ManyToManyField(User, related_name='shared_expenses')
    title = models.CharField(max_length=200)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - ${self.total_amount}"


class FamilyBudget(models.Model):
    """Model for family budgets"""
    family_members = models.ManyToManyField(User, related_name='family_budgets')
    budget_amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Family Budget: ${self.budget_amount} from {self.start_date} to {self.end_date}"


class ExpenseChallenge(models.Model):
    """Model for expense challenges among users"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    participants = models.ManyToManyField(User, related_name='expense_challenges')
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
